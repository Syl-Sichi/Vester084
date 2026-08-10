import SwiftUI

@main
struct ZELDAApp: App {
    var body: some Scene {
        WindowGroup("Z.E.L.D.A.") {
            ContentView()
        }
    }
}

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let fromUser: Bool
}

struct ContentView: View {
    private let views = ["Chat", "System", "Apps", "Files", "Security", "Settings"]
    @StateObject private var service = ZELDAServiceClient()
    @State private var selectedView = "Chat"
    @State private var message = ""
    @State private var messages: [ChatMessage] = []

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
                } else {
                    ContentUnavailableView(
                        selectedView,
                        systemImage: icon(for: selectedView),
                        description: Text("This view is ready for connection to the Z.E.L.D.A. service.")
                    )
                }
            }
            .padding()
            .task { await service.checkHealth() }
        }
        .frame(minWidth: 820, minHeight: 560)
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
