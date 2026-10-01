using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OnThiDGNL.Infrastructure.Data;

namespace OnThiDGNL.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ExamController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public ExamController(ApplicationDbContext context)
        {
            _context = context;
        }

        // DTO nhận dữ liệu nộp bài từ người dùng
        public class ExamSubmissionDto
        {
            public List<QuestionAnswerDto> Answers { get; set; }
        }

        public class QuestionAnswerDto
        {
            public int QuestionId { get; set; }
            public string SelectedAnswer { get; set; } // Ví dụ: "A", "B", "C", "D"
        }

        // API Chấm điểm bài thi (POST: api/exam/submit)
        [HttpPost("submit")]
        public async Task<IActionResult> SubmitExam([FromBody] ExamSubmissionDto submission)
        {
            if (submission == null || submission.Answers == null || !submission.Answers.Any())
            {
                return BadRequest("Bài làm không có dữ liệu trả lời.");
            }

            // Lấy danh sách ID các câu hỏi thí sinh đã trả lời
            var questionIds = submission.Answers.Select(a => a.QuestionId).ToList();

            // Truy vấn database để lấy đáp án đúng và lời giải
            var questions = await _context.Questions
                .Where(q => questionIds.Contains(q.Id))
                .ToListAsync();

            int totalQuestions = submission.Answers.Count;
            int correctCount = 0;
            var detailedResults = new List<object>();

            foreach (var answer in submission.Answers)
            {
                var question = questions.FirstOrDefault(q => q.Id == answer.QuestionId);
                if (question != null)
                {
                    // So sánh đáp án (không phân biệt hoa thường)
                    bool isCorrect = string.Equals(
                        question.CorrectAnswer?.Trim(),
                        answer.SelectedAnswer?.Trim(),
                        StringComparison.OrdinalIgnoreCase
                    );

                    if (isCorrect)
                    {
                        correctCount++;
                    }

                    // Đóng gói kết quả chi tiết từng câu
                    detailedResults.Add(new
                    {
                        questionId = question.Id,
                        content = question.Content,
                        selectedAnswer = answer.SelectedAnswer,
                        correctAnswer = question.CorrectAnswer,
                        isCorrect = isCorrect,
                        explanation = question.Explanation // Lời giải chi tiết
                    });
                }
            }

            // Tính điểm (Thang điểm 1000 giống bài thi ĐGNL hoặc tính theo phần trăm tùy ý)
            double score = Math.Round(((double)correctCount / totalQuestions) * 100, 2);

            return Ok(new
            {
                TotalQuestions = totalQuestions,
                CorrectCount = correctCount,
                ScorePercentage = score, // Điểm theo phần trăm
                Details = detailedResults
            });
        }
    }
}