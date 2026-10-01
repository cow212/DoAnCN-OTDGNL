namespace OnThiDGNL.Domain.Entities
{
    public class Question
    {
        public int Id { get; set; }
        public string Content { get; set; } = string.Empty; // Nội dung câu hỏi
        public string OptionA { get; set; } = string.Empty;
        public string OptionB { get; set; } = string.Empty;
        public string OptionC { get; set; } = string.Empty;
        public string OptionD { get; set; } = string.Empty;
        public string CorrectAnswer { get; set; } = string.Empty; // Đáp án đúng (A, B, C, D)
        public string SubjectCategory { get; set; } = string.Empty; // Phân loại (Ngôn ngữ, Toán logic, Khoa học)
        public string Explanation { get; set; } = string.Empty; // Lời giải chi tiết
    }
}