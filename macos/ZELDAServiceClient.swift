import Foundation

struct ZELDAResponse: Decodable {
    let status: String?
    let message: String?
    let error: String?
}

@MainActor
final class ZELDAServiceClient: ObservableObject {
    @Published var isConnected = false
    @Published var lastError: String?

    private let baseURL = URL(string: "http://127.0.0.1:8765")!

    func checkHealth() async {
        do {
            var request = URLRequest(url: baseURL.appendingPathComponent("health"))
            request.timeoutInterval = 2
            let (_, response) = try await URLSession.shared.data(for: request)
            isConnected = (response as? HTTPURLResponse)?.statusCode == 200
            lastError = nil
        } catch {
            isConnected = false
            lastError = error.localizedDescription
        }
    }

    func send(_ message: String) async -> String {
        do {
            var request = URLRequest(url: baseURL.appendingPathComponent("v1/message"))
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            request.httpBody = try JSONEncoder().encode(["message": message])

            let (data, response) = try await URLSession.shared.data(for: request)
            guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
                return "Z.E.L.D.A. service returned an error."
            }

            let decoded = try JSONDecoder().decode(ZELDAResponse.self, from: data)
            isConnected = true
            lastError = nil
            return decoded.message ?? decoded.error ?? "No response received."
        } catch {
            isConnected = false
            lastError = error.localizedDescription
            return "I cannot reach the Z.E.L.D.A. service right now."
        }
    }
}
