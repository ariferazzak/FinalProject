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
  form_data.append("name_give", name);

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
        window.location.reload('/user');
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

//surat kelahiran 
function save() {
    let name = $("#nama").val();
    let tempat = $("#tempat").val();
    let tanggal = $("#tanggal").val();
    let ayah = $("#ayah").val();
    let ibu = $("#ibu").val();
    let no = $("#no").val();
    let jk = $("#jk").val();
    let file = $("#formFile").val();
    $.ajax({
        type: "POST",
        url: "/pelayanan/kelahiran",
        data: {
          name : name,
          tempat : tempat,
          tanggal : tanggal,
          ayah : ayah,
          ibu : ibu,
          no : no,
          jk : jk,
          file : file
        },
        success: function (response) {
            alert("Permohonan Surat Telah Dibuat, Silahkan Cek Status!");
            window.location.replace("/homepage_user/status");
        },
        });
}

// surat domisili
function send() {
  let name = $("#nama").val();
  let ttl = $("#ttl").val();
  let jk = $("#jk").val();
  let work = $("#work").val();
  let alamat = $("#alamat").val();
  let file = $("#formFile").val();
  $.ajax({
      type: "POST",
      url: "/pelayanan/domisili",
      data: {
        name : name,
        ttl : ttl,
        jk : jk,
        work : work, 
        alamat : alamat,
        file : file,
      },
      success: function (response) {
          alert("Permohonan Surat Telah Dibuat, Silahkan Cek Status!");
          window.location.replace("/homepage_user/status");
      },
      });
}

// surat kematian
function sent() {
  let name = $("#nama").val();
  let ttl = $("#ttl").val();
  let agama = $("#agama").val();
  let jk = $("#jk").val();
  let tempat = $("#tempat").val();
  let tanggal = $("#tanggal").val();
  let penyebab = $("#penyebab").val();
  let file = $("#formFile").val();
  $.ajax({
      type: "POST",
      url: "/pelayanan/domisili",
      data: {
        name : name,
        ttl : ttl,
        agama : agama,
        jk : jk, 
        tempat : tempat,
        tanggal : tanggal,
        penyebab : penyebab,
        file : file,
      },
      success: function (response) {
          alert("Permohonan Surat Telah Dibuat, Silahkan Cek Status!");
          window.location.replace("/homepage_user/status");
      },
      });
}