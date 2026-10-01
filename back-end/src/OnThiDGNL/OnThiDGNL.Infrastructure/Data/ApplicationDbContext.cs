using Microsoft.EntityFrameworkCore;
using OnThiDGNL.Domain.Entities;

namespace OnThiDGNL.Infrastructure.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        {
        }

        // Khai báo bảng Question
        public DbSet<Question> Questions { get; set; }

        // khai bái bảng User
        public DbSet<User> Users { get; set; }
    }
}