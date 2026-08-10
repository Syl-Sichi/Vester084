import AppKit
import Foundation

@MainActor
final class NativeCommandServer: NSObject {
    private var listener: NWListener?

    func start() throws {
        let parameters = NWParameters.tcp
        let listener = try NWListener(using: parameters, on: NWEndpoint.Port(rawValue: 8766)!)
        listener.newConnectionHandler = { [weak self] connection in
            self?.handle(connection)
        }
        listener.start(queue: .main)
        self.listener = listener
    }

    private func handle(_ connection: NWConnection) {
        connection.start(queue: .main)
        receive(connection, buffer: Data())
    }

    private func receive(_ connection: NWConnection, buffer: Data) {
        connection.receive(minimumIncompleteLength: 1, maximumLength: 64 * 1024) { [weak self] data, _, isComplete, error in
            var buffer = buffer
            if let data { buffer.append(data) }

            if let error {
                connection.cancel()
                print("Z.E.L.D.A. native command error: \(error)")
                return
            }

            if isComplete || buffer.contains(10) {
                let line = buffer.split(separator: 10, maxSplits: 1).first.map(Data.init) ?? buffer
                let response = self?.execute(line) ?? ["status": "error", "message": "native server unavailable"]
                let payload = (try? JSONSerialization.data(withJSONObject: response)) ?? Data()
                connection.send(content: payload + Data([10]), completion: .contentProcessed { _ in
                    connection.cancel()
                })
                return
            }

            self?.receive(connection, buffer: buffer)
        }
    }

    private func execute(_ data: Data) -> [String: Any] {
        guard let object = try? JSONSerialization.jsonObject(with: data),
              let command = object as? [String: Any],
              let action = command["action"] as? String else {
            return ["status": "error", "message": "invalid_command"]
        }

        switch action {
        case "display.list":
            return [
                "status": "ok",
                "action": action,
                "displays": NSScreen.screens.enumerated().map { index, screen in
                    [
                        "id": "display-\(index)",
                        "name": screen.localizedName,
                        "primary": screen == NSScreen.main,
                        "width": Int(screen.frame.width),
                        "height": Int(screen.frame.height)
                    ]
                }
            ]

        case "window.move":
            guard let target = command["display"] as? String else {
                return ["status": "error", "message": "display_required"]
            }
            guard target == "primary" || NSScreen.screens.contains(where: { $0.localizedName == target }) else {
                return ["status": "error", "message": "display_not_found"]
            }
            let moved = target == "primary" ? moveToPrimary() : ZELDAWindowManager.moveToDisplay(named: target)
            return ["status": moved ? "ok" : "error", "action": action, "display": target]

        default:
            return ["status": "error", "message": "unsupported_action"]
        }
    }

    private func moveToPrimary() -> Bool {
        guard let window = ZELDAWindowManager.currentWindow(), let screen = NSScreen.main else { return false }
        let visible = screen.visibleFrame
        let size = window.frame.size
        window.setFrameOrigin(NSPoint(x: visible.midX - size.width / 2, y: visible.midY - size.height / 2))
        return true
    }
}
