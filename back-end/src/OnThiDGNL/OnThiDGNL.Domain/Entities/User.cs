using System;
using System.Collections.Generic;
using System.Text;

namespace OnThiDGNL.Domain.Entities
{
    public class User
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Password { get; set; } // Có thể mã hóa sau, hiện tại để test nhanh
        public string Role { get; set; } // "Admin" hoặc "Student"
        public string FullName { get; set; }
    }
}