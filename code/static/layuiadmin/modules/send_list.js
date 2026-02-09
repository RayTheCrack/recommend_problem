/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */ ;
layui.define(["table", "form"], function(e) {
	var t = layui.$,
		i = layui.table,
		$=layui.jquery;
	layui.form;
	i.render({
		elem: "#LAY-app-forum-list",
		url: "http://127.0.0.1:8000/send_list/",
		cols: [
			[{ field: "ID", title: "题号", width: 90, fixed: "left", align: "center" },
                { field: "Title", title: "Title" },
                { field: "Tags", title: "Tags", width: 150 },
                { field: "Rating", title: "Rating", width: 150 },
                { field: "Solved", title: "Solved", width: 150 }]
		],
		page: !0,
		limit: 15,
		limits: [15, 20, 30, 50],
		text: "对不起，加载出现异常！"
	}),  i.on("tool(LAY-app-forum-list)", function(e) {
		e.data;
		console.log(e.data.send_key)
		if("send" === e.event) layer.confirm("确定提交 "+e.data.name+" 吗？", function(t) {
			$.ajax({
				   type: 'POST',
				   data:{"problem_id":e.data.problem_id, "send_key":e.data.send_key},
				   url: '/send_problem/',
				   success: function (res) {
					   layer.msg(res.msg);location.reload()
				   },
				   error:function(response){
					   layer.msg(response.msg);
				   }
			   }),
				layer.close(t)
		});
		else if("send_1" === e.event) layer.confirm("确定取消提交 "+e.data.name+" 吗？", function(t){
			$.ajax({
				   type: 'POST',
				   data:{"problem_id":e.data.problem_id, "send_key":e.data.send_key},
				   url: '/send_problem/',
				   success: function (res) {
					   layer.msg(res.msg);location.reload()
				   },
				   error:function(response){
					   layer.msg(response.msg);
				   }
			   }),layer.close(t)
		});
	}),e("forum", {})
});
