// Cấu hình kết nối API chung tới Backend Python (port từ API .NET)
// (Bản .NET gốc: https://localhost:7162/api)
const API_BASE_URL = "http://localhost:8000/api";

async function apiRequest(endpoint, method = "GET", data = null) {
    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}/${endpoint}`, options);
        
        // Nếu API trả về lỗi (400, 401, 500...)
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || "Đã có lỗi xảy ra từ máy chủ.");
        }

        // Đọc dữ liệu JSON trả về (nếu có nội dung)
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            return await response.json();
        }
        return await response.text();
    } catch (error) {
        console.error("API Request Error:", error);
        throw error;
    }
}