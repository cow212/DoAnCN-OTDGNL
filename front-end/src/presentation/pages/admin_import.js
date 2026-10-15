// Thêm chức năng import đề thi từ file CSV, JSON, Excel trong modal "Tải đề thi".
(function () {
    const importModal = document.getElementById('importModal');
    const importFile = document.getElementById('importFile');
    const importPreview = document.getElementById('importPreview');
    const importMsg = document.getElementById('importMsg');
    const openImportBtn = document.getElementById('openImportBtn');
    const closeImportModal = document.getElementById('closeImportModal');
    const cancelImport = document.getElementById('cancelImport');
    const startImport = document.getElementById('startImport');

    if (!importModal || !openImportBtn) return;

    let parsedQuestions = [];

    function setImportMessage(text, type) {
        if (!importMsg) return;
        importMsg.textContent = text;
        importMsg.className = 'mt-3 text-center text-sm font-medium min-h-[20px] ' +
            (type === 'error' ? 'text-red-600' : type === 'success' ? 'text-emerald-600' : 'text-brand-600');
    }

    function openImport() {
        importModal.classList.remove('hidden');
        importModal.classList.add('flex');
    }

    function closeImport() {
        importModal.classList.add('hidden');
        importModal.classList.remove('flex');
        parsedQuestions = [];
        if (importFile) importFile.value = '';
        if (importPreview) importPreview.textContent = 'Chưa có file nào được chọn.';
        if (importMsg) importMsg.textContent = '';
    }

    function findField(raw, name) {
        const key = Object.keys(raw).find(k => k.toLowerCase() === name.toLowerCase());
        return key ? raw[key] : '';
    }

    function normalizeQuestion(raw) {
        return {
            Content: String(findField(raw, 'Content') || '').trim(),
            OptionA: String(findField(raw, 'OptionA') || '').trim(),
            OptionB: String(findField(raw, 'OptionB') || '').trim(),
            OptionC: String(findField(raw, 'OptionC') || '').trim(),
            OptionD: String(findField(raw, 'OptionD') || '').trim(),
            CorrectAnswer: String(findField(raw, 'CorrectAnswer') || '').trim().toUpperCase(),
            SubjectCategory: String(findField(raw, 'SubjectCategory') || 'Khac').trim(),
            Explanation: String(findField(raw, 'Explanation') || '').trim(),        ExamCode: String(findField(raw, 'ExamCode') || '').trim()
        };
    }

    function isValidQuestion(q) {
        return q.Content && q.OptionA && q.OptionB && q.OptionC && q.OptionD &&
            ['A', 'B', 'C', 'D'].includes(q.CorrectAnswer);
    }

    function renderPreview(items) {
        if (!items.length) {
            importPreview.textContent = 'Khong co du lieu hop le.';
            return;
        }
        const preview = items.slice(0, 5).map((q, i) =>
            '#' + (i + 1) + ': ' + q.Content + ' | Dap an: ' + q.CorrectAnswer + ' | Mon: ' + q.SubjectCategory
        ).join('\n');
        importPreview.textContent = 'Tong ' + items.length + ' cau. Xem truoc ' + Math.min(5, items.length) + ' cau:\n\n' + preview;
    }

    function splitCsvLine(line) {
        const result = [];
        let current = '';
        let inQuotes = false;
        for (let i = 0; i < line.length; i++) {
            const ch = line[i];
            if (ch === '"') {
                if (inQuotes && line[i + 1] === '"') {
                    current += '"';
                    i++;
                } else {
                    inQuotes = !inQuotes;
                }
            } else if (ch === ',' && !inQuotes) {
                result.push(current);
                current = '';
            } else {
                current += ch;
            }
        }
        result.push(current);
        return result.map(x => x.trim());
    }

    function parseCsv(text) {
        const lines = text.replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n').filter(l => l.trim() !== '');
        if (lines.length < 2) return [];
        const headers = splitCsvLine(lines[0]);
        const rows = [];
        for (let i = 1; i < lines.length; i++) {
            const cols = splitCsvLine(lines[i]);
            const obj = {};
            headers.forEach((h, idx) => { obj[h] = cols[idx] || ''; });
            rows.push(obj);
        }
        return rows;
    }

    window.openImport = openImport;
    openImportBtn.addEventListener('click', openImport);
    closeImportModal.addEventListener('click', closeImport);
    cancelImport.addEventListener('click', closeImport);
    importModal.addEventListener('click', (e) => { if (e.target === importModal) closeImport(); });

    importFile.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setImportMessage('Dang doc file...', 'info');
        try {
            const ext = file.name.split('.').pop().toLowerCase();
            let rawRows = [];
            if (ext === 'json') {
                const text = await file.text();
                rawRows = JSON.parse(text);
                if (!Array.isArray(rawRows)) throw new Error('File JSON phai la mang [...]');
            } else if (ext === 'csv') {
                const text = await file.text();
                rawRows = parseCsv(text);
            } else if (ext === 'xlsx' || ext === 'xls') {
                if (!window.XLSX) throw new Error('Chua tai xong thu vien Excel.');
                const buffer = await file.arrayBuffer();
                const workbook = window.XLSX.read(buffer);
                const sheetName = workbook.SheetNames[0];
                rawRows = window.XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
            } else {
                throw new Error('Chi ho tro CSV, JSON, XLSX, XLS.');
            }

            parsedQuestions = rawRows.map(normalizeQuestion);
            renderPreview(parsedQuestions);
            const validCount = parsedQuestions.filter(isValidQuestion).length;
            setImportMessage('Da doc ' + parsedQuestions.length + ' cau, hop le ' + validCount + ' cau.', validCount > 0 ? 'success' : 'error');
        } catch (err) {
            parsedQuestions = [];
            importPreview.textContent = 'Khong doc duoc file.';
            setImportMessage(err.message || 'Doc file that bai.', 'error');
        }
    });

    startImport.addEventListener('click', async () => {
        if (!parsedQuestions.length) {
            setImportMessage('Chua co du lieu de import.', 'error');
            return;
        }

        const importSubjectSelect = document.getElementById("importSubject");
        const selectedSubject = importSubjectSelect ? importSubjectSelect.value.trim() : "";
        const sourceQuestions = selectedSubject
            ? parsedQuestions.map(q => ({...q, SubjectCategory: selectedSubject}))
            : parsedQuestions;
        const validQuestions = sourceQuestions.filter(isValidQuestion);
        if (!validQuestions.length) {
            setImportMessage('Khong co cau hoi hop le de import.', 'error');
            return;
        }

        const user = JSON.parse(localStorage.getItem('user') || '{}');
        const token = user.AccessToken;
        if (!token) {
            alert('Phien dang nhap da het han. Vui long dang nhap lai.');
            window.location.href = 'login.html';
            return;
        }

        setImportMessage('Dang import ' + validQuestions.length + ' cau hoi...', 'info');
        let success = 0;
        let fail = 0;
        for (const q of validQuestions) {
            try {
                const res = await fetch('http://localhost:8000/api/Questions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify(q)
                });
                if (!res.ok) throw new Error(await res.text());
                success++;
            } catch (err) {
                fail++;
            }
        }
        setImportMessage('Hoan tat import: ' + success + ' thanh cong, ' + fail + ' that bai.', fail ? 'error' : 'success');
        if (typeof window.loadQuestions === 'function') window.loadQuestions();
    });
})();
