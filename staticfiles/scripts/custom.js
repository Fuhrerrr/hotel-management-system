$(document).ready(function(){
    
    // Add To Selection
    $(".add-to-selection").on("click", function(){

        let button = $(this)
        let id = button.attr("data-index")

        let hotel_id = $("#id").val()
        let room_id = $(`.room_id_${id}`).val()
        let room_number = $(`.room_number_${id}`).val()
        let hotel_name = $("#hotel_name").val()
        let room_name = $("#room_name").val()
        let room_price = $("#room_price").val()
        let number_of_beds = $("#number_of_beds").val()
        let room_type = $("#room_type").val()
        let checkin = $("#checkin").val()
        let checkout = $("#checkout").val()
        let adult = $("#adult").val()
        let children = $("#children").val()

        console.log(`${id} Added To Selection`);
        console.log(`hotel_id: ${hotel_id}`);
        console.log(`room_number: ${room_number}`);
        console.log(`room_id: ${room_id}`);
        console.log(`hotel_name: ${hotel_name}`);
        console.log(`room_name: ${room_name}`);
        console.log(`room_price: ${room_price}`);
        console.log(`number_of_beds: ${number_of_beds}`);
        console.log(`room_type: ${room_type}`);
        console.log(`checkin: ${checkin}`);
        console.log(`checkout: ${checkout}`);
        console.log(`adult: ${adult}`);
        console.log(`children: ${children}`);


        $.ajax({
            url:'/booking/add_to_selection/',
            data: {
                'id': id,
                'hotel_id': hotel_id,
                'hotel_name': hotel_name,
                'room_number': room_number,
                'room_name': room_name,
                'room_price': room_price,
                'number_of_beds': number_of_beds,
                'room_type': room_type,
                'room_id': room_id,
                'checkin': checkin,
                'checkout': checkout,
                'adult': adult,
                'children': children,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Adding room...");
                button.html("<i class='fas fa-clock-rotate-left'></i> Adding room... ")
            },
            success: function(response){
                button.html("<i class='fas fa-check-circle'></i> Added to selection ")

                console.log("Added Room To Selection!");
                $(".room-count").text(response.total_selected_items)
                
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 1000,
                    timerProgressBar: true,
                })
                    
                Toast.fire({
                    icon: 'success',
                    title: 'Added Room To Selection!'
                })
            }
        })

    })

    // Delete item from cart
	$(document).on('click','.delete-item',function(){
		var id = $(this).attr('data-item');
		var button = $(this);
		
		$.ajax({
			url:'/booking/delete_selection/',
			data:{
				'id':id,
			},
			dataType:'json',
			beforeSend:function(){
				button.text('...');
			},
			success:function(res){
				$(".room-count").text(res.total_selected_items);
				$(".selection-list").html(res.data);

                if (res.total_selected_items < 1) {
                    Swal.fire({
                        icon: 'warning',
                        title: 'No Selections Yet...',
                        text: "Add some selection to continue to cart..."
                    }).then((result) => {
                        window.location.href = "/"
                      });

                    
                }
			}
		});
	}); 

    $(document).on('change', '#noti-status', function(){
        const query = $(this).val()
        
        $.ajax({
            url:"/dashboard/notification_filter/",
            beforeSend: function(){
                console.log("Sending Data...");
            },
            data: {
                "query": query
            },
            success: function(res){
                console.log(res.data);
				$(".noti-div-main").html(res.data);

            }
        })
    })

    // Mark Notification As Seen
    $(document).on('click', '.mark-noti-as-seen', function(){
        let button = $(this)
        let id = button.attr("data-index")
        console.log(id);
        $.ajax({
            url:"/dashboard/notification_mark_as_seen/",
            beforeSend: function(){
                console.log("Sending Data...");
            },
            data: {
                "id": id
            },
            success: function(res){
                $(".noti-div-"+id).addClass("d-none")
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 1000,
                    timerProgressBar: true,
                })
                    
                Toast.fire({
                    icon: 'success',
                    title: 'Notification Seen!'
                })
            }
        })
    })

    // Add to bookmark
    $(document).on('click', '#add-to-bookmark', function(){
        let button = $(this)
        let id = button.attr("data-hotel")
        console.log(id);

        $.ajax({
            url:"/dashboard/add_to_bookmark/",
            beforeSend: function(){
                button.html('<i class="fas fa-spinner fa-spin" style="color: gray;"></i>')
            },
            data: {
                "id": id
            },
            success: function(res){
                $(".noti-div-"+id).addClass("d-none")
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 1000,
                    timerProgressBar: true,
                })
                    
                Toast.fire({
                    icon: res.icon,
                    title: res.data
                })

                if (res.data == "Bookmark Deleted") {
                    button.html('<i class="fas fa-heart" style="color: gray;"></i>')
                } else {
                    button.html('<i class="fas fa-heart" style="color: red;"></i>')
                }

                if (res.data == "Login To Bookmark Hotel") {
                    button.html('<i class="fas fa-heart" style="color: gray;"></i>')
                } 
            }
        })
    })

    // Add Review and Rating
    $(document).on('click', '#review-btn', function(){
        let button = $(this)
        let id = button.attr("data-hotel")
        let review = $("#review-input").val()
        let rating = $("#rating-input").val()
        console.log(rating);

        $.ajax({
            url:"/dashboard/add_review/",
            beforeSend: function(){
                button.html('<i class="fas fa-spinner fa-spin" style="color: white;"></i>')
            },
            data: {
                "id": id,
                "review": review,
                "rating": rating,
            },
            success: function(res){
                const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 1000,
                    timerProgressBar: true,
                })
                    
                Toast.fire({
                    icon: res.icon,
                    title: res.data
                })

                $("#add-review-button").hide()
                $("#review_div").html('Review submitted successfully <i class="fas fa-check-circle"></i> ')
                
            }
        })
    })

    function makeAjaxCall() {
        $.ajax({
            url: '/update_room_status/',  
            type: 'GET',
            success: function(data) {
                console.log("Checked Rooms");
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log('Error:', errorThrown);
            }
        });
    }

    setInterval(makeAjaxCall, 60000);
    // makeAjaxCall();
})

