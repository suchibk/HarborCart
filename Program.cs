using System.Collections.Concurrent;
using System.ComponentModel.DataAnnotations;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
var registrations = new ConcurrentDictionary<string, Guid>(StringComparer.OrdinalIgnoreCase);

app.UseDefaultFiles();
app.UseStaticFiles();

app.MapPost("/api/registrations", (RegistrationRequest request) =>
{
    var errors = new Dictionary<string, string[]>();
    if (string.IsNullOrWhiteSpace(request.FirstName) || request.FirstName.Trim().Length > 80)
        errors["firstName"] = ["First name is required and must be at most 80 characters."];
    if (string.IsNullOrWhiteSpace(request.LastName) || request.LastName.Trim().Length > 80)
        errors["lastName"] = ["Last name is required and must be at most 80 characters."];
    if (request.Age is null || request.Age <= 18 || request.Age > 120)
        errors["age"] = ["Age must be a whole number between 18 and 120."];
    if (string.IsNullOrWhiteSpace(request.Email) || request.Email.Trim().Length > 254 ||
        !new EmailAddressAttribute().IsValid(request.Email.Trim()))
        errors["email"] = ["Enter a valid email address (at most 254 characters)."];

    if (string.IsNullOrWhiteSpace(request.ConfirmEmail) ||
        !string.Equals(request.Email?.Trim(), request.ConfirmEmail.Trim(), StringComparison.OrdinalIgnoreCase))
        errors["confirmEmail"] = ["Confirm Email must match your email address."];

    if (errors.Count > 0)
        return Results.ValidationProblem(errors);

    var email = request.Email!.Trim();
    var customerId = Guid.NewGuid();
    if (!registrations.TryAdd(email, customerId))
        return Results.Conflict(new { message = "This email address is already registered." });

    return Results.Json(new
    {
        customerId,
        message = $"Welcome to HarborStore, {request.FirstName!.Trim()}!"
    }, statusCode: StatusCodes.Status201Created);
});

app.Run();

public sealed record RegistrationRequest(string? FirstName, string? LastName, int? Age, string? Email, string? ConfirmEmail);
