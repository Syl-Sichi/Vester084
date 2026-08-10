import SwiftUI
import AppKit

@main
struct ZELDAApp: App {
    @StateObject private var nativeServer = NativeServerState()

    var body: some Scene {
        WindowGroup("Z.E.L.D.A.") {
            ContentView()
                .task {
                    nativeServer.start()
                }
        }
    }
}

@MainActor
final class NativeServerState: ObservableObject {
    private let server = NativeCommandServer()
    @Published var isRunning = false

    func start() {
        guard !isRunning else { return }
        do {
            try server.start()
            isRunning = true
        } catch {
            print("Z.E.L.D.A. native command server failed: \(error)")
        }
    }
}

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let fromUser: Bool
}

struct DisplayRecord: Identifiable {
    let id: String
    let name: String
    let isPrimary: Bool
    let width: Int
    let height: Int
}

struct ContentView: View {
    private let views = ["Chat", "System", "Apps", "Files", "Security", "Settings"]
    @StateObject private var service = ZELDAServiceClient()
    @State private var selectedView = "Chat"
    @State private var message = ""
    @State private var messages: [ChatMessage] = []
    @State private var displays: [DisplayRecord] = []

    var body: some View {
        NavigationSplitView {
            List(views, id: \.self, selection: $selectedView) { item in
                Label(item, systemImage: icon(for: item))
            }
            .navigationTitle("Z.E.L.D.A.")
        } detail: {
            VStack(alignment: .leading, spacing: 16) {
                HStack {
                    Text(selectedView)
                        .font(.title2.bold())
                    Spacer()
                    Label(
                        service.isConnected ? "Connected" : "Offline",
                        systemImage: service.isConnected ? "circle.fill" : "circle"
                    )
                    .foregroundStyle(.secondary)
                }

                if selectedView == "Chat" {
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 10) {
                            if messages.isEmpty {
                                Text("Good morning. How can I help?")
                                    .font(.title3)
                            }
                            ForEach(messages) { item in
                                HStack {
                                    if item.fromUser { Spacer() }
                                    Text(item.text)
                                        .padding(10)
                                        .background(item.fromUser ? Color.accentColor.opacity(0.15) : Color.secondary.opacity(0.12))
                                        .clipShape(RoundedRectangle(cornerRadius: 12))
                                    if !item.fromUser { Spacer() }
                                }
                            }
                        }
                    }

                    HStack {
                        TextField("Ask Z.E.L.D.A.", text: $message)
                            .textFieldStyle(.roundedBorder)
                            .onSubmit { sendMessage() }
                        Button("Send") { sendMessage() }
                            .buttonStyle(.borderedProminent)
                            .disabled(message.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                    }
                } else if selectedView == "System" {
                    systemView
                } else {
                    ContentUnavailableView(
                        selectedView,
                        systemImage: icon(for: selectedView),
                        description: Text("This view is ready for connection to the Z.E.L.D.A. service.")
                    )
                }
            }
            .padding()
            .task {
                await service.checkHealth()
                refreshDisplays()
            }
        }
        .frame(minWidth: 820, minHeight: 560)
    }

    private var systemView: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                Text("Displays")
                    .font(.headline)

                if displays.isEmpty {
                    Text("No display information available.")
                        .foregroundStyle(.secondary)
                } else {
                    ForEach(displays) { display in
                        HStack {
                            Image(systemName: display.isPrimary ? "display" : "rectangle.on.rectangle")
                            VStack(alignment: .leading) {
                                Text(display.name)
                                Text("\(display.width) × \(display.height)")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                            Spacer()
                            if display.isPrimary {
                                Text("Primary")
                                    .font(.caption)
                                    .foregroundStyle(.secondary)
                            }
                        }
                        .padding()
                        .background(Color.secondary.opacity(0.08))
                        .clipShape(RoundedRectangle(cornerRadius: 10))
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    private func refreshDisplays() {
        displays = NSScreen.screens.enumerated().map { index, screen in
            let frame = screen.frame
            return DisplayRecord(
                id: screen.localizedName + "-\(index)",
                name: screen.localizedName,
                isPrimary: screen == NSScreen.main,
                width: Int(frame.width),
                height: Int(frame.height)
            )
        }
    }

    private func sendMessage() {
        let text = message.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty else { return }
        message = ""
        messages.append(ChatMessage(text: text, fromUser: true))

        Task {
            let response = await service.send(text)
            messages.append(ChatMessage(text: response, fromUser: false))
        }
    }

    private func icon(for item: String) -> String {
        switch item {
        case "Chat": return "bubble.left.and.bubble.right"
        case "System": return "desktopcomputer"
        case "Apps": return "square.grid.2x2"
        case "Files": return "folder"
        case "Security": return "lock.shield"
        case "Settings": return "gearshape"
        default: return "circle"
        }
    }
}
