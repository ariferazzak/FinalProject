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

// edit profil
function update_profile() {
  let name = $("#username_update").val();
  let file = $("#picture")[0].files[0];
  let form_data = new FormData();
  form_data.append("file_give", file);
  form_data.append("longname_give", name);

  $.ajax({
    type: "POST",
    url: "/update_profile",
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      if (response["result"] === "success") {
        alert(response["msg"]);
        window.location.reload();
      }
    },
  });
}

// logout
function sign_out() {
  $.removeCookie("mytoken", { path: "/" });
  alert("Signed out!");
  window.location.href = "/login/user";
}

// batal surat kelahiran

function batal(birthId) {
  $.ajax({
    url: '/user/delete_birth/' + birthId,
    type: 'POST',
    success: function(response) {
      if (response.result === 'success') {
        alert('Permohonan berhasil dibatalkan');
        window.location.reload();
      } else {
        console.log('Failed to delete :', response.msg);
      }
    },
    error: function(xhr, status, error) {
      console.log('Error:', error);
    }
  });
}

// batal surat domisili

function hapus(domisiliId) {
  $.ajax({
    url: '/user/delete_domisili/' + domisiliId,
    type: 'POST',
    success: function(response) {
      if (response.result === 'success') {
        alert('Permohonan berhasil dibatalkan');
        window.location.reload();
      } else {
        console.log('Failed to delete :', response.msg);
      }
    },
    error: function(xhr, status, error) {
      console.log('Error:', error);
    }
  });
}

// batal surat domisili

function cancel(dieId) {
  $.ajax({
    url: '/user/delete_die/' + dieId,
    type: 'POST',
    success: function(response) {
      if (response.result === 'success') {
        alert('Permohonan berhasil dibatalkan');
        window.location.reload();
      } else {
        console.log('Failed to delete :', response.msg);
      }
    },
    error: function(xhr, status, error) {
      console.log('Error:', error);
    }
  });
}

