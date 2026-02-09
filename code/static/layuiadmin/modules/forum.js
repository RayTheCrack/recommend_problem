layui.define(["table", "form"], function (e) {
    var t = layui.$,
        i = layui.table,
        $ = layui.jquery;
    layui.form;

    // 渲染表格
    i.render({
        elem: "#LAY-app-forum-list",  // 表格元素
        url: "http://127.0.0.1:8000/get_problem_list/",  // 获取数据的接口
        cols: [
            [
                { field: "ID", title: "题号", width: 90, fixed: "left", align: "center" },
                { field: "Title", title: "Title" },
                { field: "Tags", title: "Tags", width: 150 },
                { field: "Rating", title: "Rating", width: 150 },
                { field: "Solved", title: "Solved", width: 150 },
                {
                    field: 'send_key',
                    title: "操作",
                    width: 130,
                    align: "center",
                    fixed: "right",
                    toolbar: "#table-forum-list"  // 自定义操作栏
                }
            ]
        ],
        page: true,  // 启用分页
        limit: 15,
        limits: [15, 20, 30, 50],
        text: "对不起，加载出现异常！"
    });

    // 表格操作事件监听
    i.on("tool(LAY-app-forum-list)", function (e) {
        e.data;
        console.log(e.data.send_key);

        // 投递操作
        if ("send" === e.event) {
            layer.confirm("确定提交 " + e.data.Title + " 吗？", function (t) {
                $.ajax({
                    type: 'POST',
                    data: { "problem_id": e.data.ID, "send_key": e.data.send_key },
                    url: '/send_problem/',  // 请求的 URL
                    success: function (res) {
                        layer.msg(res.msg);
                        location.reload();  // 刷新页面
                    },
                    error: function (response) {
                        layer.msg(response.msg);
                    }
                });
                layer.close(t);
            });
        }
        // 取消投递操作
        else if ("send_1" === e.event) {
            layer.confirm("确定取消提交 " + e.data.Title + " 吗？", function (t) {
                $.ajax({
                    type: 'POST',
                    data: { "problem_id": e.data.ID, "send_key": e.data.send_key },
                    url: '/send_problem/',  // 请求的 URL
                    success: function (res) {
                        layer.msg(res.msg);
                        location.reload();  // 刷新页面
                    },
                    error: function (response) {
                        layer.msg(response.msg);
                    }
                });
                layer.close(t);
            });
        }
    });

    e("forum", {});
});
