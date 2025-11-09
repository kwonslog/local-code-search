package main

import (
	"encoding/json"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", rootHandler) // 👈 루트 핸들러 추가
	http.HandleFunc("/metadata", metadataHandler)
	http.HandleFunc("/health", healthHandler)

	port := ":8080"
	log.Printf("✅ MCP Server started on %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}

// 루트 핸들러: ChatGPT 커넥터 탐색용
func rootHandler(w http.ResponseWriter, r *http.Request) {
	resp := map[string]interface{}{
		"name":     "Local Go MCP Server",
		"version":  "1.0.0",
		"protocol": "MCP/1.0",
		"endpoints": map[string]string{
			"/metadata": "Server metadata info",
			"/health":   "Server health status",
		},
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func metadataHandler(w http.ResponseWriter, r *http.Request) {
	resp := map[string]interface{}{
		"name":     "Local Go MCP Server",
		"version":  "1.0.0",
		"protocol": "MCP/1.0",
		"capabilities": []string{
			"directory.list", "file.read", "file.write",
		},
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	resp := map[string]string{
		"status":  "ok",
		"message": "MCP server is alive",
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}
