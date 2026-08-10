import SwiftUI

@main
struct ZELDAApp: App {
    var body: some Scene {
        WindowGroup("Z.E.L.D.A.") {
            ContentView()
        }
    }
}

struct ContentView: View {
    private let views = ["Chat", "System", "Apps", "Files", "Security", "Settings"]
    @State private var selectedView = "Chat"
    @State private var message = ""

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
                    Label("Ready", systemImage: "circle.fill")
                        .foregroundStyle(.secondary)
                }

                if selectedView == "Chat" {
                    Spacer()
                    Text("Good morning. How can I help?")
                        .font(.title3)
                    Spacer()

                    HStack {
                        TextField("Ask Z.E.L.D.A.", text: $message)
                            .textFieldStyle(.roundedBorder)
                        Button("Send") {
                            message = ""
                        }
                        .buttonStyle(.borderedProminent)
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
        }
        .frame(minWidth: 820, minHeight: 560)
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
