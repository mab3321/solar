document.addEventListener("DOMContentLoaded", function () {
  let sortLinks = document.querySelectorAll(".sort-link");

  sortLinks.forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      let sortField = this.dataset.sort;
      let currentUrl = new URL(window.location.href);
      let sortParam = currentUrl.searchParams.get("sort_by");

      if (sortParam === sortField) {
        // If already sorted by the same field, toggle sorting direction
        sortParam = sortParam.startsWith("-") ? sortField : "-" + sortField;
      } else {
        // Otherwise, default to ascending order
        sortParam = sortField;
      }

      currentUrl.searchParams.set("sort_by", sortParam);
      window.location.href = currentUrl.toString();
    });
  });
});
