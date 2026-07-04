/* ====================================================================
 * 8ET OMNI-CONSOLE - SERVICE WORKER INFRASTRUCTURE v5.0
 * ==================================================================== */

const CACHE_NAME = '8et-matrix-cache-v5';

// 定義需要徹底鎖定在 PS4 本機快取硬碟中的檔案清單
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './exploit.js',
  // 核心與常用系統工具
  './payloads/goldhen_2.4b16.bin',
  './payloads/ftp.bin',
  './payloads/app2usb.bin',
  // 安全與維護工具
  './payloads/disableupdate.bin',
  './payloads/enableupdate.bin',
  './payloads/todex.bin',
  './payloads/historyblocker.bin',
  // 遊戲修改、金手指與 Dumper 備份
  './payloads/webrte.bin',
  './payloads/ps4debug.bin',
  './payloads/dumper.bin',
  './payloads/gtav_lefter_900.bin',
  './payloads/rdr2_mod.bin',
  './payloads/backup.bin',
  './payloads/restore.bin'
];

// 1. 安裝階段：強行將所有資源抓下來塞進 PS4 瀏覽器緩衝區
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[Worker] 正在執行多容量二進位 Payload 快取鎖定...');
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// 2. 啟用階段：清理舊版本的快取資料
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('[Worker] 清理過期快取配置...');
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. 攔截請求階段（核心關鍵）：就算斷網，也無條件從 PS4 硬碟讀取快取檔案
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // 如果硬碟快取有，就直接回傳快取，速度極快且支援 100% 離線
      if (response) {
        return response;
      }
      // 如果快取沒有（例如未來新加的檔案），才嘗試走網路下載
      return fetch(event.request);
    })
  );
});
