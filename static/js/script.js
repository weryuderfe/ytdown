document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('downloadForm');
    const formatBtns = document.querySelectorAll('.format-btn');
    const downloadBtn = document.getElementById('downloadBtn');
    const btnText = downloadBtn.querySelector('.btn-text');
    const spinner = downloadBtn.querySelector('.spinner');
    const historyList = document.getElementById('historyList');
    
    let downloadHistory = JSON.parse(localStorage.getItem('downloadHistory') || '[]');
    updateHistoryDisplay();

    // Format button handlers
    formatBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            formatBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = document.getElementById('url').value;
        const format = document.querySelector('.format-btn.active').dataset.format;
        const quality = document.getElementById('quality').value;

        if (!url) {
            alert('Please enter a YouTube URL');
            return;
        }

        // Show loading state
        downloadBtn.disabled = true;
        btnText.textContent = 'Downloading...';
        spinner.classList.remove('hidden');

        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url, format, quality }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Download failed');
            }

            // Add to history
            const historyItem = { url, format, quality, timestamp: new Date().toISOString() };
            downloadHistory.unshift(historyItem);
            if (downloadHistory.length > 10) downloadHistory.pop();
            localStorage.setItem('downloadHistory', JSON.stringify(downloadHistory));
            updateHistoryDisplay();

            // Reset form
            form.reset();
            document.querySelector('.format-btn[data-format="mp4"]').classList.add('active');
            document.querySelector('.format-btn[data-format="mp3"]').classList.remove('active');
            
            alert('Download completed successfully!');
        } catch (error) {
            alert(error.message);
        } finally {
            // Reset button state
            downloadBtn.disabled = false;
            btnText.textContent = 'Download';
            spinner.classList.add('hidden');
        }
    });

    function updateHistoryDisplay() {
        historyList.innerHTML = downloadHistory.map(item => `
            <div class="history-item">
                <div class="history-url">${item.url}</div>
                <div class="history-format">${item.format.toUpperCase()} - ${item.quality}</div>
            </div>
        `).join('');
    }
});