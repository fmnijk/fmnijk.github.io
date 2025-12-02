/*上方隱藏的按鈕*/
document.addEventListener('keydown', function (event) {
    if (event.key.toLowerCase() === 'h') {
        let buttons = document.getElementsByClassName('hiddenButton');
        for (let i = 0; i < buttons.length; i++) {
            buttons[i].style.display = (buttons[i].style.display === 'inline-flex') ? 'none' : 'inline-flex';
        }
    }
});

/*圖片搜尋工具*/
document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const imageUrl = document.getElementById('image-url');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const searchLinks = document.querySelectorAll('.search-buttons a');

    // 更新所有連結的 href
    function updateSearchLinks(imageUrl) {
        searchLinks.forEach(link => {
            let baseUrl, searchUrl;

            switch (link.id) {
                case 'saucenao':
                    baseUrl = `https://saucenao.com/`;
                    searchUrl = `https://saucenao.com/search.php?db=999&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'danbooru':
                    baseUrl = `https://danbooru.donmai.us/`;
                    searchUrl = `https://danbooru.donmai.us/iqdb_queries?url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-lens-tw':
                    baseUrl = `https://www.google.com/?olud=`;
                    searchUrl = `https://lens.google.com/uploadbyurl?safe=off&gl=tw&hl=zh-TW&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-lens-cn':
                    baseUrl = `https://www.google.com/?olud=`;
                    searchUrl = `https://lens.google.com/uploadbyurl?safe=off&gl=cn&hl=zh-CN&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-lens-ja':
                    baseUrl = `https://www.google.com/?olud=`;
                    searchUrl = `https://lens.google.com/uploadbyurl?safe=off&gl=ja&hl=ja&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-lens-ko':
                    baseUrl = `https://www.google.com/?olud=`;
                    searchUrl = `https://lens.google.com/uploadbyurl?safe=off&gl=kr&hl=ko&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-lens-us':
                    baseUrl = `https://www.google.com/?olud=`;
                    searchUrl = `https://lens.google.com/uploadbyurl?safe=off&gl=us&hl=en-US&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-image-search-tw':
                    baseUrl = `https://images.google.com/`;
                    searchUrl = `https://www.google.com/searchbyimage?safe=off&gl=tw&hl=zh-TW&sbisrc=google&image_url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-image-search-cn':
                    baseUrl = `https://images.google.com/`;
                    searchUrl = `https://www.google.com/searchbyimage?safe=off&gl=cn&hl=zh-CN&sbisrc=google&image_url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-image-search-ja':
                    baseUrl = `https://images.google.com/`;
                    searchUrl = `https://www.google.com/searchbyimage?safe=off&gl=ja&hl=ja&sbisrc=google&image_url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-image-search-ko':
                    baseUrl = `https://images.google.com/`;
                    searchUrl = `https://www.google.com/searchbyimage?safe=off&gl=kr&hl=ko&sbisrc=google&image_url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'google-image-search-us':
                    baseUrl = `https://images.google.com/`;
                    searchUrl = `https://www.google.com/searchbyimage?safe=off&gl=us&hl=en-US&sbisrc=google&image_url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'yandex':
                    baseUrl = `https://yandex.ru/images/`;
                    searchUrl = `https://yandex.ru/images/touch/search?rpt=imageview&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'bing':
                    baseUrl = `https://www.bing.com/`;
                    searchUrl = `https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIVSP&sbisrc=UrlPaste&q=imgurl:${encodeURIComponent(imageUrl)}`;
                    break;
                case 'tineye':
                    baseUrl = `https://www.tineye.com/`;
                    searchUrl = `https://www.tineye.com/search/?url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'iqdb':
                    baseUrl = `https://iqdb.org/`;
                    searchUrl = `https://iqdb.org/?url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'iqdb-3d':
                    baseUrl = `https://3d.iqdb.org/`;
                    searchUrl = `https://3d.iqdb.org/?url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'ascii2d-net':
                    baseUrl = `https://ascii2d.net/`;
                    searchUrl = `https://ascii2d.net/search/url/${encodeURIComponent(imageUrl)}`;
                    break;
                case 'trace-moe':
                    baseUrl = `https://trace.moe/`;
                    searchUrl = `https://trace.moe/?auto&url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'baidu':
                    baseUrl = `https://graph.baidu.com/pcpage/index?tpl_from=pc`;
                    searchUrl = `https://graph.baidu.com/details?isfromtusoupc=1&tn=pc&carousel=0&promotion_name=pc_image_shituindex&extUiData%5bisLogoShow%5d=1&image=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'sogou':
                    baseUrl = `https://pic.sogou.com/`;
                    searchUrl = `https://ris.sogou.com/ris?query=https%3A%2F%2Fimg03.sogoucdn.com%2Fv2%2Fthumb%2Fretype_exclude_gif%2Fext%2Fauto%3Fappid%3D122%26url%3D${encodeURIComponent(imageUrl)}&flag=1&drag=1`;
                    break;
                case 'alamy':
                    baseUrl = `https://www.alamy.com/`;
                    searchUrl = `https://www.alamy.com/search.html?imageurl=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'immerse':
                    baseUrl = `https://www.immerse.zone/`;
                    searchUrl = `https://www.immerse.zone/image-search?url=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'lexica':
                    baseUrl = `https://lexica.art/`;
                    searchUrl = `https://lexica.art/?q=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'karmadecay':
                    baseUrl = `http://karmadecay.com/`;
                    searchUrl = `http://karmadecay.com/search?q=${encodeURIComponent(imageUrl)}`;
                    break;
                case 'imgops':
                    baseUrl = `https://imgops.com/`;
                    let imgopsUrl = imageUrl.replace(/^https?:\/\//, '');
                    searchUrl = `https://imgops.com/${imgopsUrl}`;
                    break;
                case 'taobao':
                    baseUrl = `https://world.taobao.com/`;
                    searchUrl = `https://world.taobao.com/`;
                    break;
                case '1688':
                    baseUrl = `https://www.1688.com/`;
                    searchUrl = `https://www.1688.com/`;
                    break;
                case '360':
                    baseUrl = `https://image.so.com/`;
                    searchUrl = `https://image.so.com/`;
                    break;
                case 'wildberries':
                    baseUrl = `https://www.wildberries.ru/`;
                    searchUrl = `https://www.wildberries.ru/`;
                    break;
                case 'e-hentai':
                    baseUrl = `https://e-hentai.org/`;
                    searchUrl = `https://e-hentai.org/`;
                    break;
                default:
                    searchUrl = baseUrl = '';
            }

            link.href = imageUrl ? searchUrl : baseUrl;
        });
    }

    updateSearchLinks('');

    // 監聽 input 變化
    imageUrl.addEventListener('input', () => {
        const url = imageUrl.value.trim();
        updateSearchLinks(url);
        if (url) {
            showImagePreview(url);
        } else {
            hideImagePreview();
        }
    });

    // 上傳圖片後更新連結
    async function handleImage(file, maxRetries = 3) {
        imageUrl.value = '壓縮並上傳中...';
        // 預覽原始圖片並調暗
        showImagePreview(URL.createObjectURL(file));
        dimImagePreview();

        // --- 壓縮圖片的程式碼開始 ---
        console.log(`原始圖片大小: ${(file.size / 1024 / 1024).toFixed(2)} MB`);

        const options = {
            maxSizeMB: 1,           // 控制輸出檔案的最大體積 (單位 MB)
            maxWidthOrHeight: 1920, // 控制輸出圖片的最長邊像素
            useWebWorker: true,     // 使用 Web Worker，避免 UI 卡頓
            fileType: 'image/jpeg', // 強制輸出為 JPG 格式
            initialQuality: 1.0     // 初始壓縮品質
        }

        let compressedFile;
        try {
            // 呼叫函式庫進行壓縮
            compressedFile = await imageCompression(file, options);
            console.log(`壓縮後圖片大小: ${(compressedFile.size / 1024 / 1024).toFixed(2)} MB`);
        } catch (error) {
            console.error('圖片壓縮失敗:', error);
            showToast(`圖片壓縮失敗: ${error.message}`);
            imageUrl.value = '壓縮失敗，請重試';
            // 恢復預覽圖亮度
            imagePreview.style.opacity = 1.0;
            return;
        }
        // --- 壓縮圖片的程式碼結束 ---

        // 使用壓縮後的圖片 (compressedFile) 進行上傳
        const formData = new FormData();
        formData.append('image', compressedFile);
        formData.append('key', '091241c47103f1746809646d2d4aef7f');
        formData.append('expiration', 15552000); // 180 days in seconds

        let retries = 0;
        while (retries < maxRetries) {
            try {
                const response = await fetch('https://api.imgbb.com/1/upload', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const result = await response.json();

                if (result.data && result.data.url) {
                    imageUrl.value = result.data.url;
                    // 使用 imgbb 返回的 URL 更新預覽圖並恢復亮度
                    showImagePreview(result.data.url);
                    updateSearchLinks(result.data.url);
                    return;
                } else {
                    throw new Error('Upload failed: No URL in response');
                }
            } catch (error) {
                console.error(`Error uploading image (attempt ${retries + 1}):`, error);
                retries++;

                if (retries === maxRetries) {
                    showToast(`上傳圖片時發生錯誤：${error.message}`);
                    imageUrl.value = '上傳失敗，請重試';
                    // 恢復預覽圖亮度
                    imagePreview.style.opacity = 1.0;
                } else {
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            }
        }
    }

    dropZone.addEventListener('click', () => fileInput.click());

    document.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    document.addEventListener('dragleave', (e) => {
        // 只有當離開到文檔外部時才移除效果
        if (!e.relatedTarget || e.relatedTarget.nodeName === 'HTML') {
            dropZone.classList.remove('dragover');
        }
    });

    document.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImage(file);
        }
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImage(file);
        }
    });

    function showImagePreview(url) {
        imagePreview.src = url;
        imagePreview.style.opacity = 1.0;
        previewContainer.style.display = 'block';
    }

    function hideImagePreview() {
        imagePreview.src = "";
        previewContainer.style.display = 'none';
    }

    function dimImagePreview() {
        imagePreview.style.opacity = 0.5;
    }

    function showToast(message) {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.position = 'fixed';
        toast.style.bottom = '20px';
        toast.style.left = '50%';
        toast.style.transform = 'translateX(-50%)';
        toast.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        toast.style.color = 'white';
        toast.style.padding = '10px 20px';
        toast.style.borderRadius = '5px';
        toast.style.zIndex = '1000';

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
});