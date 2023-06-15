// Edit Profil
function update_profile() {
    let name = $("#username_update").val();
    let file = $("#picture")[0].files[0];
    let form_data = new FormData();
    form_data.append("file_give", file);
    form_data.append("name_give", name);

    $.ajax({
      type: "POST",
      url: "/update_profile",
      data: {
        form_data,
        id: id, 
    },
      cache: false,
      contentType: false,
      processData: false,
      success: function (response) {
        if (response["result"] === "success") {
          alert(response["msg"]);
          window.location.reload('/user');
        }
      },
    });
  }

// logout
  function sign_out(){
    $.removeCookie('mytoken', {path: '/user'});
    alert('Signed out!');
    window.location.href = "{{ url_for('loginUser') }}";
  }

// Send Pengaduan
function simpan() {
    let name = $("#name").val();
    let pengaduan = $("#pengaduan").val();
    let kejadian = $("#tanggal").val();
    let file = $("#formFile").val();
    let today = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/posting",
        data: {
            username_give:name,
            pengaduan_give:pengaduan,
            file_give: file,
            kejadian_give : kejadian, 
            date_give :today
        },
        success: function (response) {
            alert("Pengaduan Anda Telah di Kirim!");
            window.location.replace("/user");
        },
        });
}

function pengaduan(){
    $.ajax({
        type: "GET",
        url: "/login/user",
        data: {
            username_give: username,
            pw_give: password,
        },
        success: function (response) {
            if (response["result"] === "success") {
            $.cookie("mytoken", response["token"], { path: "/user" });
            window.location.replace("/user");
            } else {
            alert(response["msg"]);
            }
        },
        });
}