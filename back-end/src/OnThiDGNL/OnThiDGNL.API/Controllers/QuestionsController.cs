using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OnThiDGNL.Domain.Entities;
using OnThiDGNL.Infrastructure.Data;

namespace OnThiDGNL.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class QuestionsController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public QuestionsController(ApplicationDbContext context)
        {
            _context = context;
        }

        // 1. API Lấy danh sách toàn bộ câu hỏi (GET: api/questions)
        [HttpGet]
        public async Task<IActionResult> GetAllQuestions()
        {
            var questions = await _context.Questions.ToListAsync();
            return Ok(questions);
        }

        // 2. API Thêm mới một câu hỏi (POST: api/questions)
        [HttpPost]
        public async Task<IActionResult> CreateQuestion([FromBody] Question question)
        {
            if (question == null)
            {
                return BadRequest("Dữ liệu câu hỏi không hợp lệ.");
            }

            _context.Questions.Add(question);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetAllQuestions), new { id = question.Id }, question);
        }
    }
}