/*  Auto-insert Django CSRF token into every <form method="post">  */
(function () {
  function getCookie(name) {
    const cookie = document.cookie
      .split(";")
      .map(c => c.trim())
      .find(c => c.startsWith(name + "="));
    return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
  }

  document.addEventListener("DOMContentLoaded", () => {
    const token = getCookie("csrftoken");
    if (!token) return;       // no cookie, nothing to do

    document.querySelectorAll("form[method='post']").forEach(form => {
      if (form.querySelector("input[name='csrfmiddlewaretoken']")) return; // already present

      const hidden = document.createElement("input");
      hidden.type  = "hidden";
      hidden.name  = "csrfmiddlewaretoken";
      hidden.value = token;
      form.appendChild(hidden);
    });
  });
})();
