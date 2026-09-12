const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
let pollInterval;

const form = document.getElementById('researchForm');
const companyInput = document.getElementById('companyInput');
const searchBtn = document.getElementById('searchBtn');
const btnText = document.querySelector('.btn-text');
const btnSpinner = document.getElementById('btnSpinner');

const statusContainer = document.getElementById('statusContainer');
const statusText = document.getElementById('statusText');
const progressBar = document.getElementById('progressBar');
const jobIdSpan = document.getElementById('jobId');
const resultAction = document.getElementById('resultAction');
const downloadLink = document.getElementById('downloadLink');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const companyName = companyInput.value.trim();
    if (!companyName) return;

    // Reset UI
    setLoadingState(true);
    statusContainer.classList.remove('hidden', 'status-completed');
    resultAction.classList.add('hidden');
    statusText.innerText = 'Initializing AI Agents...';
    progressBar.style.width = '10%';
    
    try {
        // Start Research
        const response = await fetch(`${API_BASE_URL}/research`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ company_name: companyName })
        });
        
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        const jobId = data.job_id;
        jobIdSpan.innerText = jobId;
        
        // Start Polling
        startPolling(jobId);
    } catch (error) {
        console.error('Error:', error);
        statusText.innerText = 'Error starting research. Is the server running?';
        statusText.style.color = '#ef4444';
        setLoadingState(false);
    }
});

function startPolling(jobId) {
    let progress = 20;
    
    // Clear any existing intervals
    if (pollInterval) clearInterval(pollInterval);
    
    pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/status/${jobId}`);
            const data = await response.json();
            
            if (data.status === 'Pending') {
                statusText.innerText = 'Waiting in Queue...';
                progressBar.style.width = '30%';
            } 
            else if (data.status === 'Processing') {
                statusText.innerText = 'AI Agents are analyzing data...';
                // Fake progress increment for visual effect
                progress = progress >= 90 ? 90 : progress + 10;
                progressBar.style.width = `${progress}%`;
            } 
            else if (data.status === 'Completed') {
                clearInterval(pollInterval);
                statusText.innerText = 'Report Generated Successfully!';
                progressBar.style.width = '100%';
                
                statusContainer.classList.add('status-completed');
                
                // Show dashboard and render markdown
                const reportDashboard = document.getElementById('reportDashboard');
                const markdownContent = document.getElementById('markdownContent');
                const resultAction = document.getElementById('resultAction');
                
                reportDashboard.classList.remove('hidden');
                resultAction.classList.remove('hidden');
                
                if (data.report_content) {
                    markdownContent.innerHTML = marked.parse(data.report_content);
                } else {
                    markdownContent.innerHTML = "<p>No content generated.</p>";
                }
                
                setLoadingState(false);
            } 
            else if (data.status === 'Failed') {
                clearInterval(pollInterval);
                statusText.innerText = 'Research Failed.';
                statusText.style.color = '#ef4444';
                progressBar.style.width = '100%';
                progressBar.style.background = '#ef4444';
                setLoadingState(false);
            }
        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 2000); // Poll every 2 seconds
}

function setLoadingState(isLoading) {
    if (isLoading) {
        searchBtn.disabled = true;
        btnText.classList.add('hidden');
        btnSpinner.classList.remove('hidden');
        companyInput.disabled = true;
    } else {
        searchBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnSpinner.classList.add('hidden');
        companyInput.disabled = false;
    }
}
