import AppKit

@MainActor
enum ZELDAWindowManager {
    static func currentWindow() -> NSWindow? {
        NSApp.windows.first { window in
            window.isVisible && window.title == "Z.E.L.D.A."
        }
    }

    static func moveToPrimaryDisplay() {
        guard let window = currentWindow(), let screen = NSScreen.main else { return }
        move(window, to: screen)
    }

    static func moveToDisplay(named name: String) -> Bool {
        guard let window = currentWindow(),
              let screen = NSScreen.screens.first(where: { $0.localizedName == name }) else {
            return false
        }
        move(window, to: screen)
        return true
    }

    private static func move(_ window: NSWindow, to screen: NSScreen) {
        let visible = screen.visibleFrame
        let size = window.frame.size
        let origin = NSPoint(
            x: visible.midX - size.width / 2,
            y: visible.midY - size.height / 2
        )
        window.setFrameOrigin(origin)
    }
}
