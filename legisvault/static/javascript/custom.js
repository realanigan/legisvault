$(document).ready(function () {
  const modalTitle = $("#modalTitle");
  const modalBody = $("#modalBody");

  $(".councellor").on("click", function () {
    let id = $(this).data("id");

    $.ajax({
      url: `/legislator/${id}`,
      method: "GET",
      success: function (response) {
        modalTitle.html(response.name);
        modalBody.html(response.bio);
      },
      error: function (xhr, status, error) {
        console.error("Error fetching data: ", error);
      },
    });
  });
});
