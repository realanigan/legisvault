const modal = document.getElementById("default-modal");
const modalInstance = new Modal(modal); // Requires Flowbite Modal to be imported

$(document).ready(function () {
  const modalTitle = $("#modalTitle");
  const modalBody = $("#modalBody");

  $(".councellor").on("click", function () {
    let id = $(this).data("id");

    modalTitle.html(`
      <div role="status" class="max-w-sm animate-pulse align-middle flex">
        <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 self-center"></div>
          <span class="sr-only">Loading...</span>
        </div>`);

    modalBody.html(`
    <div role="status" class="max-w-sm animate-pulse">
      <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-48 mb-4"></div>
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2.5"></div>
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
      <span class="sr-only">Loading...</span>
    </div>`);

    $.ajax({
      url: `/legislator/${id}`,
      method: "GET",
      success: function (response) {
        modalTitle.html(response.name);
        modalBody.html(response.bio);
      },
      error: function (xhr, status, error) {
        modalTitle.html("Error");
        modalBody.html("Can't Load Any Data");
      },
    });
  });
});
