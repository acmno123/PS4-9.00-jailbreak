import http.server
import socketserver
import socket
import urllib.parse

PORT = 8080

class MyExploitServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 解析網址，看前端是不是傳來了選擇 Payload 的請求
        parsed_url = urllib.parse.urlparse(self.path)
        
        if parsed_url.path == "/select_payload":
            # 取得網頁傳來的參數 (例如 ?type=ftp)
            query = urllib.parse.parse_qs(parsed_url.query)
            payload_type = query.get('type', ['goldhen'])[0]
            
            print(f"[+] 一樓 PS4 選擇了功能: {payload_type}")
            
            # 根據選項決定要傳送的 bin 檔案路徑
            # 根據一樓點擊的按鈕，決定要發送 payloads 夾裡的哪一個 .bin 檔案
            bin_map = {
                "goldhen_24b16":   "payloads/goldhen.bin",
                "hen_214":         "payloads/hen214.bin",
                "webrte":          "payloads/webrte.bin",
                "ps4debug":        "payloads/ps4debug.bin",
                "dumper":          "payloads/dumper.bin",
                "ftp":             "payloads/ftp.bin",
                "orbisafv":        "payloads/orbisafv.bin",
                "backup":          "payloads/backup.bin",
                "restore":         "payloads/restore.bin",
                "todex":           "payloads/todex.bin",
                "fanctrl":         "payloads/fancontrol.bin",
                "disable_update":  "payloads/disableupdate.bin"
            }
            
            # 取得 PS4 的 IP 位址
            ps4_ip = self.client_address[0]
            
            # 回應網頁
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
            
            # 異步或直接觸發 Socket 傳送二進位檔給一樓 PS4 的 9020 Port
            self.send_bin_to_ps4(ps4_ip, target_bin)
            return
            
        # 如果不是特殊請求，就正常吐出 index.html 網頁
        return super().do_GET()

    def send_bin_to_ps4(self, ip, file_path):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            # 建立連接傳送檔案
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.connect((ip, 9020))
            s.sendall(data)
            s.close()
            print(f"[+] 成功將 {file_path} 送達一樓 PS4！")
        except Exception as e:
            print(f"[-] 傳送 bin 失敗: {e}")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyExploitServer) as httpd:
        print(f"[*] 炫酷多功能破解伺服器已在 Port {PORT} 啟動！")
        httpd.serve_forever()