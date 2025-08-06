function Design() {
    var self = this;
    // this.init = function () {
    //     self.bind_event();
    // }
    this.init = function (recordid){
        var container = $('#Design');
        var url = "http://222.118.20.236:8077?recordid=" + recordid;
        var iframe = `<iframe src="${url}" frameborder="0" width="100%" class="iframe mb-0" style="height: calc(100% - .3rem); border:none;"></iframe>`;
        container.append(iframe)
    }   

    this.bind_event = function () {
        $('#Design .btn-upload').on('click', function () {
            $("#uploadFileModal").modal("show");
        })

        // 监听文件上传框变化事件
        $('#fileupload-dropzone').change(function () {
            const file = this.files[0];
            if (file) {
                const fileType = getFileType(file.name);
                const listItem = createListItem(file.name, fileType, file.size);
                $('#uploadList').append(listItem);
            }
        });
    }

    // 根据文件名获取文件类型
    function getFileType(fileName) {
        const extension = fileName.split('.').pop().toLowerCase();

        if (extension === 'pdf') {
            return 'PDF';
        } else if (extension === 'doc' || extension === 'docx') {
            return 'Docx';
        } else if (extension === 'ppt' || extension === 'pptx') {
            return 'PowerPoint';
        } else if (extension === '.xls' || extension === '.xlsx') {
            return 'Excel';
        } else if (extension === 'jpg' || extension === 'jpeg' || extension === 'png') {
            return 'Image';
        } else {
            return 'Unknown';
        }
    }

    // 创建新的列表项
    function createListItem(fileName, fileType, fileSize) {
        let tileClass = '';
        let iconClass = '';

        if (fileType === 'PDF') {
            tileClass = 'bg-teal';
            iconClass = 'fa-file-pdf';
        } else if (fileType === 'Docx' || fileType === 'docx') {
            tileClass = 'bg-blue';
            iconClass = 'fa-file-word';
        } else if (fileType === 'Excel' || fileType === 'xlsx') {
            tileClass = 'bg-green';
            iconClass = 'fa-file-excel';
        } else if (fileType === 'PowerPoint' || fileType === 'pptx') {
            tileClass = 'bg-red';
            iconClass = 'fa-file-powerpoint';
        } else if (fileType === 'Image' || fileType === 'jpg' || fileType === 'jpeg' || fileType === 'png') {
            tileClass = 'bg-pink';
            iconClass = 'fa-file-image';
        } else {
            tileClass = 'bg-gray'; // Default class for unknown file types
            iconClass = 'fa-file';
        }

        const progressBar = $('<div class="progress progress-sm flex-fill mr-3">').append('<div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>');
        const progressDiv = $('<div class="list-group-item-body py-2 d-flex align-items-center align-self-stretch progressDiv"></div>').append(progressBar).append('<span class="text-primary"></span>');

        function updateProgressBar(progress) {
            const progressBarElement = progressBar.find('.progress-bar');
            progressBarElement.css('width', progress + '%');
            progressBarElement.attr('aria-valuenow', progress);
            progressBarElement.parent().next('span').text(progress + '%');

            if (progress === 100) {
                progressBar.addClass('fade');
                progressDiv.find('span').addClass('fade');
            } else {
                progressBar.removeClass('fade');
                progressDiv.find('span').removeClass('fade');
            }
        }

        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            updateProgressBar(progress);

            if (progress >= 100) {
                clearInterval(interval);
            }
        }, 1000);

        const deleteBtn = $('<button class="btn btn-sm btn-icon btn-light"><i class="far fa-trash-alt"></i></button>');
        const deleteBtnWrap = $('<div class="list-group-item-figure"></div>').append(deleteBtn);

        deleteBtn.click(function () {
            listItem.remove();
        });

        const listItem = $('<div class="list-group-item align-items-start">');
        listItem.append('<div class="list-group-item-figure pl-1">' +
            '<a href="#" class="tile tile-circle ' + tileClass + '"><span class="fa ' + iconClass + '"></span></a>' +
            '</div>');
        listItem.append('<div class="list-group-item-body py-2 flex-fill">' +
            '<h4 class="list-group-item-title text-truncate"><a href="#">' + fileName + '</a></h4>' +
            '<div class="d-flex align-items-center">' +
            '<p class="list-group-item-text">' + fileType + '</p>' +
            '<span class="mx-2 font-weight-bolder"> · </span>' +
            '<p class="list-group-item-text small">' + (fileSize / (1024 * 1024)).toFixed(2) + ' MB</p>' +
            '</div>' +
            '</div>');
        listItem.append(progressDiv);
        listItem.append(deleteBtnWrap);

        return listItem;
    }

    // $(function () {
    //     var documentsData = [
    //         { title: "Business services", imgUrl: "../../static/DevPlat/assets/images/temp.png", date: "Updated 1 hour ago", size: "0.59 MB" },
    //         { title: "Testing", imgUrl: "../../static/DevPlat/assets/images/temp.png", date: "Updated 2 hour ago", size: "1 MB" },
    //     ];

    //     $.each(documentsData, function (index, document) {
    //         var listItem = $("<div>").addClass("list-group-item");
    //         listItem.append(
    //             $("<div>").addClass("list-group-item-figure").append(
    //                 $("<span>").addClass("tile tile-img toggle-fullscreen").append(
    //                     $("<img>").attr("src", document.imgUrl).attr("alt", ""),
    //                     $("<div>").addClass("close-button").append(
    //                         $("<i>").addClass("fa fa-times").css("font-size", "18px")
    //                     )
    //                 )
    //             ),
    //             $("<div>").addClass("list-group-item-body").append(
    //                 $("<h4>").addClass("list-group-item-title").html('<a href="#">' + document.title + '</a>'),
    //                 $("<div>").addClass("d-flex align-items-center").append(
    //                     $("<p>").addClass("list-group-item-text uploadFileDate position-relative pr-4").text(document.date),
    //                     $("<p>").addClass("list-group-item-text small").text(document.size)
    //                 )
    //             ),
                
    //             $("<div>").addClass("list-group-item-figure").append(
    //                 $("<div>").addClass("dropdown").append(
    //                     $("<button>").addClass("btn btn-sm btn-icon btn-light")
    //                         .attr("data-toggle", "dropdown")
    //                         .attr("aria-expanded", "false")
    //                         .append($("<i>").addClass("fa fa-fw fa-ellipsis-v")),
    //                     $("<div>").addClass("dropdown-menu dropdown-menu-right").append(
    //                         $("<div>").addClass("dropdown-arrow mr-n1"),
    //                         $("<button>").addClass("dropdown-item").attr("type", "button").text("Download"),
    //                         $("<button>").addClass("dropdown-item").attr("type", "button").text("View details"),
    //                         $("<button>").addClass("dropdown-item").attr("type", "button").text("Share file"),
    //                         $("<button>").addClass("dropdown-item").attr("type", "button").text("Copy link file"),
    //                         $("<div>").addClass("dropdown-divider"),
    //                         $("<button>").addClass("dropdown-item").attr("type", "button").text("Remove")
    //                     )
    //                 )
    //             ))

    //         $("#documentContainer").append(listItem);

    //         $(".toggle-fullscreen").click(function () {
    //             $(this).toggleClass("fullscreen");
    //         });
    //     });

    //     $.each(documentsData, function (index, item) {
    //         var cardWrap = $('<div>').addClass('col-lg-6 col-xl-3 ');
    //         var card = $('<div>').addClass('card card-fluid');
    //         var cardHeader = $('<div>').addClass('card-header border-0');
    //         var headerContent = $('<div>').addClass('d-flex justify-content-between align-items-center');
    //         var badge = $('<span>').addClass('badge bg-white').text(item.size);
    //         var dropdownDiv = $('<div>').addClass('dropdown');
    //         var dropdownButton = $('<button>').addClass('btn btn-icon btn-light').attr({ 'type': 'button', 'data-toggle': 'dropdown', 'aria-expanded': 'false' }).html('<i class="fa fa-ellipsis-v"></i>');
    //         var dropdownMenu = $('<div>').addClass('dropdown-menu dropdown-menu-right');
    //         var dropdownArrow = $('<div>').addClass('dropdown-arrow');
    //         var editLink = $('<a>').addClass('dropdown-item').attr('href', '#').text('Edit');
    //         var removeLink = $('<a>').addClass('dropdown-item').attr('href', '#').text('Remove');
    //         var cardBody = $('<div>').addClass('card-body text-center');
    //         var userAvatar = $('<a>').addClass('user-avatar user-avatar-xl').attr('href', '#');
    //         var avatarImage = $('<img>').attr({ 'src': item.imgUrl, 'alt': '' });
    //         var cardTitle = $('<h5>').addClass('card-title mt-3').html('<a href="#">' + item.title + '</a>');
    //         var cardSubtitle = $('<p>').addClass('card-subtitle text-muted').text(item.date);

    //         headerContent.append(badge, dropdownDiv.append(dropdownButton, dropdownMenu.append(dropdownArrow, editLink, removeLink)));
    //         userAvatar.append(avatarImage);
    //         cardBody.append(userAvatar, cardTitle, cardSubtitle);
    //         card.append(cardHeader.append(headerContent), cardBody);
    //         cardWrap.append(card);
            
    //         $('#fileGrid>.row').append(cardWrap);
    //     });
    // })
}