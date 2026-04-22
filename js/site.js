(function () {
  var themes = {
    light: "#2563eb",
    mint: "#0f9f6e",
    ink: "#f59e0b"
  };
  var savedTheme = localStorage.getItem("site-theme") || "light";
  var savedAccent = localStorage.getItem("site-accent");
  var buttons = document.querySelectorAll("[data-theme-choice]");
  var picker = document.getElementById("accentPicker");

  function applyTheme(theme, accent) {
    document.body.dataset.theme = theme;
    document.documentElement.style.setProperty("--accent", accent || themes[theme] || themes.light);
    buttons.forEach(function (button) {
      button.classList.toggle("active", button.dataset.themeChoice === theme);
    });
    if (picker) {
      picker.value = accent || themes[theme] || themes.light;
    }
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var theme = button.dataset.themeChoice;
      localStorage.setItem("site-theme", theme);
      localStorage.removeItem("site-accent");
      applyTheme(theme);
    });
  });

  if (picker) {
    picker.addEventListener("input", function () {
      localStorage.setItem("site-accent", picker.value);
      document.documentElement.style.setProperty("--accent", picker.value);
    });
  }

  applyTheme(savedTheme, savedAccent);
})();
