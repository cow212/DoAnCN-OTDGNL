using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using OnThiDGNL.Domain.Entities;
using OnThiDGNL.Infrastructure.Data;
using System.Text.RegularExpressions; // Thêm namespace này để dùng Regex

namespace OnThiDGNL.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly ApplicationDbContext _context;

        public AuthController(ApplicationDbContext context)
        {
            _context = context;
        }

        public class LoginDto
        {
            public string Username { get; set; }
            public string Password { get; set; }
        }

        public class RegisterDto
        {
            public string Username { get; set; }
            public string Password { get; set; }
            public string FullName { get; set; }
        }

        // 1. API ĐĂNG KÝ VỚI VALIDATION CHẶT CHẼ
        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegisterDto model)
        {
            if (model == null || string.IsNullOrEmpty(model.Username) || string.IsNullOrEmpty(model.Password))
            {
                return BadRequest("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.");
            }

            // 1. Kiểm tra mật khẩu phải có ít nhất 1 chữ số và 1 ký tự đặc biệt
            bool hasNumber = Regex.IsMatch(model.Password, @"[0-9]");
            bool hasSpecialChar = Regex.IsMatch(model.Password, @"[!@#$%^&*(),.?:{}|<>\-_+=~`[\]\\/]");

            if (!hasNumber || !hasSpecialChar)
            {
                return BadRequest("Mật khẩu bảo mật yếu: Phải chứa ít nhất một chữ số và một ký tự đặc biệt!");
            }

            // 2. Kiểm tra xem Username đã có người đăng ký chưa
            var userExists = await _context.Users.AnyAsync(u => u.Username == model.Username);
            if (userExists)
            {
                return BadRequest("Tên đăng nhập này đã có người đăng ký. Vui lòng chọn tên khác!");
            }

            // 3. Tạo tài khoản mới
            var newUser = new User
            {
                Username = model.Username,
                Password = model.Password, // Lưu ý thực tế sẽ hash password sau
                FullName = model.FullName,
                Role = "Student" // Mặc định học sinh
            };

            _context.Users.Add(newUser);
            await _context.SaveChangesAsync();

            return Ok(new { Message = "Đăng ký tài khoản thành công! Bạn có thể đăng nhập ngay bây giờ." });
        }

        // 2. API ĐĂNG NHẬP
        [HttpPost("login")]
        public async Task<IActionResult> Login([FromBody] LoginDto model)
        {
            if (model == null || string.IsNullOrEmpty(model.Username) || string.IsNullOrEmpty(model.Password))
            {
                return BadRequest("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.");
            }

            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.Username == model.Username && u.Password == model.Password);

            if (user == null)
            {
                return Unauthorized("Tài khoản hoặc mật khẩu không chính xác.");
            }

            return Ok(new
            {
                Message = "Đăng nhập thành công!",
                UserId = user.Id,
                Username = user.Username,
                FullName = user.FullName,
                Role = user.Role
            });
        }
    }
}