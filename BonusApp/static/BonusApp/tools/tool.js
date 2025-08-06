
var projectName = "/Forum";
/*獲取cookie*/
function getCookie(key) {
	var strCookie = document.cookie;
	var arr = strCookie.split(";");
	for (var i = 0; i < arr.length; i++) {
		var t = arr[i].split("=");
		if (t[0].trim() == key) {
			return t[1];
		}
	}
}

function getParam(key) {
	var strParam = location.search;
	if (strParam != null) {
		var arr = strParam.slice(1).split("&");
		for (var i = 0; i < arr.length; i++) {
			var t = arr[i].split("=");
			if (t[0].trim() == key) {
				return t[1];
			}
		}
	}
}

/**
 * 設置cookie
 * @returns
 */
function setCookie(key, value) {
	document.cookie = key + "=" + value;
}

function removeCookie(key) {
	var exp = new Date();
	exp.setTime(exp.getTime() - 1);
	if (getCookie(key) != null) {
		document.cookie = key + "=123;expires=" + exp.toGMTString();
	}
}

function getAgoDay(number) {
	var now = parseInt(new Date().getTime() / 1000);
	var theTime = parseInt(number / 1000);
	if (now - theTime > 60) {//
		now /= 60;
		theTime /= 60;
		if (now - theTime > 60) {//分
			now /= 60;
			theTime /= 60;
			if (now - theTime > 24) {//時
				now /= 24;
				theTime /= 24;
				if (now - theTime > 30) {//天
					now /= 30;
					theTime /= 30;
					if (now - theTime > 12) {//月
						now /= 12;
						theTime /= 12;
						return parseInt(now - theTime) + " year ago"
					} else {
						return parseInt(now - theTime) + " month ago";
					}
				} else {
					return parseInt(now - theTime) + " day ago"
				}
			} else {
				return parseInt(now - theTime) + " hour ago"
			}
		} else {
			return parseInt(now - theTime) + " minute ago"
		}
	} else {
		if (parseInt(now - theTime) <= 0) {
			return "1 second ago"
		} else {
			return parseInt(now - theTime) + " second ago"
		}
	}
}

function formatNumTime(date) {
	var year = date.slice(0, 4);
	var month = date.slice(4, 6);
	var day = date.slice(date.length - 2);
	return year + '-' + month + '-' + day
}

/**
 * 格式化對話時間
 * @param number
 * @returns
 */
function formatChatTime(number) {
	var now = new Date();
	var theTime = new Date(parseInt(number));
	var year = theTime.getFullYear();
	var month = theTime.getMonth() + 1;
	var date = theTime.getDate();
	var hours = theTime.getHours();
	var minutes = theTime.getMinutes();
	var seconds = theTime.getSeconds();
	if (month < 10) {
		month = "0" + month
	}
	if (date < 10) {
		date = "0" + date;
	}
	if (hours < 10) {
		hours = "0" + hours
	}
	if (minutes < 10) {
		minutes = "0" + minutes
	}
	if (seconds < 10) {
		seconds = "0" + seconds
	}
	if (now.getFullYear() == theTime.getFullYear() && now.getMonth() + 1 == theTime.getMonth() + 1 && now.getDate() - theTime.getDate() <= 2) {
		if (theTime.getDate() - now.getDate() == 0) {
			return hours + ":" + minutes;
		} else if (now.getDate() - theTime.getDate() == 1) {
			return "昨天";
		} else {
			return "前天";
		}
	} else {
		return theTime.getFullYear() + "-" + month + "-" + date;
	}
}

function formatChatTime2(number) {
	var now = new Date();
	var theTime = new Date(parseInt(number));
	var year = theTime.getFullYear();
	var month = theTime.getMonth() + 1;
	var date = theTime.getDate();
	var hours = theTime.getHours();
	var minutes = theTime.getMinutes();
	var seconds = theTime.getSeconds();
	if (month < 10) {
		month = "0" + month
	}
	if (date < 10) {
		date = "0" + date;
	}
	if (hours < 10) {
		hours = "0" + hours
	}
	if (minutes < 10) {
		minutes = "0" + minutes
	}
	if (seconds < 10) {
		seconds = "0" + seconds
	}

	return theTime.getFullYear() + "-" + month + "-" + date;

}

/**
 * 格式化時間  如：2019-03-01 20:30:10
 * @param number
 * @returns
 */
function formatTime(number) {

	var date = new Date(parseInt(number));
	var year = date.getFullYear();
	var month = date.getMonth() + 1;
	var day = date.getDate();
	var hours = date.getHours();
	var minutes = date.getMinutes();
	var seconds = date.getSeconds();
	if (month < 10) {
		month = "0" + month
	}
	if (day < 10) {
		day = "0" + day;
	}
	if (hours < 10) {
		hours = "0" + hours
	}
	if (minutes < 10) {
		minutes = "0" + minutes
	}
	if (seconds < 10) {
		seconds = "0" + seconds
	}
	return year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
}



function getFrmWidth(b) {
	var clientWidth = document.documentElement.clientWidth;
	var width = clientWidth * b;
	if (clientWidth <= 678) {
		width = clientWidth;
	}
	return width;
}

function froalaBug(discussionCon) {
	var obj = $('<div>' + discussionCon + '</div>');
	var conObj = obj.children();
	for (var i = 0; i < conObj.length; i++) {
		if ($(conObj[i]).attr("data-f-id") == "pbf") {
			$(conObj[i]).remove();
		}
	}
	return obj.html();
}

/**
 * 分頁樣式
 * @returns
 */
function toClass() {
	$(".pagination").children().each(function (index, item) {
		$(item).attr('class', $(item).attr('class') + ' un page-link-gx');
	})
}

function dateFormat(fmt, date) {
	let ret;
	const opt = {
		"Y+": date.getFullYear().toString(),        // 年
		"m+": (date.getMonth() + 1).toString(),     // 月
		"d+": date.getDate().toString(),            // 日
		"H+": date.getHours().toString(),           // 时
		"M+": date.getMinutes().toString(),         // 分
		"S+": date.getSeconds().toString()          // 秒
		// 有其他格式化字符需求可以继续添加，必须转化成字符串
	};
	for (let k in opt) {
		ret = new RegExp("(" + k + ")").exec(fmt);
		if (ret) {
			fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
		};
	};
	return fmt;
}

function parseDjangoTime(dateStr) {
	var dayArray = dateStr.substr(0, 10).split('-')
	var timeArray = dateStr.substr(11, 8).split(':')
	var date = new Date()
	date.setFullYear(parseInt(dayArray[0]))
	date.setMonth(parseInt(dayArray[1]) - 1)
	date.setDate(parseInt(dayArray[2]))
	date.setHours(parseInt(timeArray[0]))
	date.setMinutes(parseInt(timeArray[1]))
	date.setSeconds(parseInt(timeArray[2]))
	return date.getTime()
}

function JsonSort(json, key) {   //console.log(json);
	for (var j = 1, jl = json.length; j < jl; j++) {
		var temp = json[j],
			val = parseInt(temp[key]),
			i = j - 1;
		while (i >= 0 && parseInt(json[i][key]) < val) {
			json[i + 1] = json[i];
			i = i - 1;
		}
		json[i + 1] = temp;

	}
	console.log(json);
	return json;
}





/**
 * 全局過濾器，頭像路徑問題
 */
// Vue.filter('replaceAvatarUrl', function (url) {
// 	if (url.indexOf("timg.jpg") != -1) {
// 		url = url.replace("/Forum", "/static");
// 		//url = "/static" + url
// 	}
// 	return url;
// })
