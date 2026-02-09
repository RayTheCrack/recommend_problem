/** layuiAdmin.std-v1.0.0 LPPL License By http://www.layui.com/admin/ */
;
layui.define(function (exports) {
    $ = layui.jquery;

    $.ajax({
        type: 'GET',
        url: '/get_pie/',  // 请求数据接口
        success: function (res) {
            console.log(res.rating_data)
            var tag_data = res.tag_data;
            var rating_data = res.rating_data;

            layui.use(["carousel", "echarts"], function () {
                var e = layui.$;
                var a = layui.echarts;
                var l = [];
                var t = [{
                    title: {
                        text: "标签分布和难度分布",
                        x: "center",
                        textStyle: {
                            fontSize: 14
                        }
                    },
                    tooltip: {
                        trigger: "item",
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                    series: [{
                        name: "标签分布",
                        type: "pie",
                        radius: "70%",
                        center: ["25%", "50%"],  // 左边饼图
                        data: tag_data
                    }, {
                        name: "难度分布",
                        type: "pie",
                        radius: "70%",
                        center: ["75%", "50%"],  // 右边饼图
                        data: rating_data
                    }]
                }];

                var i = e("#LAY-index-dataview").children("div");
                var n = function (e) {
                    l[e] = a.init(i[e], layui.echartsTheme);
                    l[e].setOption(t[e]);
                    window.onresize = l[e].resize;
                };

                // 确保页面中存在至少一个 div 来放置图表
                if (i[0]) n(0);
            });
        },
        error: function (response) {
            layer.msg('数据加载失败');
        }
    });

    exports('index', {});


    layui.use(["admin", "carousel"], function () {
        var e = layui.$,
            t = (layui.admin, layui.carousel),
            a = layui.element,
            i = layui.device();
        e(".layadmin-carousel").each(function () {
            var a = e(this);
            t.render({
                elem: this,
                width: "100%",
                arrow: "none",
                interval: a.data("interval"),
                autoplay: a.data("autoplay") === !0,
                trigger: i.ios || i.android ? "click" : "hover",
                anim: a.data("anim")
            })
        }), a.render("progress")
    }), layui.use(["carousel", "echarts"], function () {
        var e = layui.$,
            $ = layui.jquery,
            a = (layui.carousel, layui.echarts),
            l = [],
            t = [{
                series: [
                    {
                        name: 'Pressure',
                        type: 'gauge',
                        radius: '70%',
                        axisLine: {
                            lineStyle: {
                                width: 4 // 这个是修改宽度的属性
                            }
                        },
                        center: ['25%', '50%'],
                        progress: {
                            show: true
                        },
                        detail: {
                            valueAnimation: true,
                            formatter: '{value}%',
                            textStyle: {
                                fontSize: 20
                            }
                        },
                        data: [
                            {
                                value: 0,
                                name: 'CPU使用率'
                            }
                        ],
                        splitLine: {
                            lineStyle: {
                                width: 1
                            }
                        },
                        title: {
                            offsetCenter: [0, '30%']//设置位置
                        }
                    },
                    {
                        name: 'Pressure',
                        type: 'gauge',
                        radius: '70%',
                        axisLine: {
                            lineStyle: {
                                width: 4 // 这个是修改宽度的属性
                            }
                        },
                        center: ['75%', '50%'],
                        progress: {
                            show: true
                        },
                        detail: {
                            valueAnimation: true,
                            formatter: '{value}%',
                            textStyle: {
                                fontSize: 20
                            }
                        },
                        data: [
                            {
                                value: 0,
                                name: '内存使用率'
                            }
                        ],
                        splitLine: {
                            lineStyle: {
                                width: 1
                            }
                        },
                        title: {
                            offsetCenter: [0, '30%']//设置位置
                        }
                    }
                ]
            },],
            i = e("#LAY-index-control").children("div"),
            n = function (e) {
                l[e] = a.init(i[e], layui.echartsTheme), l[e].setOption(t[e]), window.onresize = l[e].resize
            };
        i[0] && n(0);
        setInterval(function () {
            $.ajax({
                type: 'GET',
                url: '/get_psutil/',
                success: function (res) {
                    t[0].series[0].data[0].value = (res.cpu_data).toFixed(2) - 0;
                    t[0].series[1].data[0].value = (res.memory_data).toFixed(2) - 0;
                    l[0].setOption(t[0]);
                },
                error: function (response) {
                    layer.msg(response.msg);
                }
            })
        }, 30000);
    }), layui.use("table", function () {
        var e = (layui.$, layui.table);
        e.render({
            elem: "#LAY-index-topSearch",
            url: layui.setter.base + "json/console/top-search.js",
            page: !0,
            cols: [
                [{
                    type: "numbers",
                    fixed: "left"
                }, {
                    field: "keywords",
                    title: "关键词",
                    minWidth: 300,
                    templet: '<div><a href="https://www.baidu.com/s?wd={{ d.keywords }}" target="_blank" class="layui-table-link">{{ d.keywords }}</div>'
                }, {
                    field: "frequency",
                    title: "搜索次数",
                    minWidth: 120,
                    sort: !0
                }, {
                    field: "userNums",
                    title: "用户数",
                    sort: !0
                }]
            ],
            skin: "line"
        }), e.render({
            elem: "#LAY-index-topCard",
            url: layui.setter.base + "json/console/top-card.js",
            page: !0,
            cellMinWidth: 120,
            cols: [
                [{
                    type: "numbers",
                    fixed: "left"
                }, {
                    field: "title",
                    title: "标题",
                    minWidth: 300,
                    templet: '<div><a href="{{ d.href }}" target="_blank" class="layui-table-link">{{ d.title }}</div>'
                }, {
                    field: "username",
                    title: "发帖者"
                }, {
                    field: "channel",
                    title: "类别"
                }, {
                    field: "crt",
                    title: "点击率",
                    sort: !0
                }]
            ],
            skin: "line"
        })
    }), e("console", {})
});