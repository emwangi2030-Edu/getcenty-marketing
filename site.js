(function () {
  var toggle = document.querySelector(".nav-menu-toggle");
  var panel = document.getElementById("nav-menu-panel");
  if (!toggle || !panel) return;

  function setOpen(open) {
    panel.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("nav-menu-open", open);
  }

  toggle.addEventListener("click", function () {
    setOpen(!panel.classList.contains("is-open"));
  });

  panel.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      setOpen(false);
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });
})();
