// document.getElementsByTagName('title')[0].innerHTML = val;
// window.setDocumentTitle = function(title) {
//   var i = document.createElement('iframe');
//   i.src = '../favicon.ico';
//   i.style.display = 'none';
//   i.onload = function() {
//     setTimeout(function(){
//       i.remove();
//     }, 9)
//   }
//   document.body.appendChild(i);
// };//ios
const common = {
    changeTitle: function (val) {
        document.getElementsByTagName('title')[0].innerHTML = val;
        window.setDocumentTitle = function (title) {
            var i = document.createElement('iframe');
            i.src = '../favicon.ico';
            i.style.display = 'none';
            i.onload = function () {
                setTimeout(function () {
                    i.remove();
                }, 9)
            }
            document.body.appendChild(i);
        };//ios
    },
    GetQueryString(name) {
        var url = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var newUrl = window.location.search.substr(1).match(url);
        if (newUrl != null) {
            return unescape(newUrl[2]);
        } else {
            return false;
        }
    },
    getScrollTop() {
        var scrollTop = 0;
        if (document.documentElement && document.documentElement.scrollTop) {
            scrollTop = document.documentElement.scrollTop;
        } else if (document.body) {
            scrollTop = document.body.scrollTop;
        }
        return scrollTop;
    },
    // 获取当前可视范围的高度
    getClientHeight() {
        var clientHeight = 0;
        if (document.body.clientHeight && document.documentElement.clientHeight) {
            clientHeight = Math.min(document.body.clientHeight, document.documentElement.clientHeight);
        }
        else {
            clientHeight = Math.max(document.body.clientHeight, document.documentElement.clientHeight);
        }
        return clientHeight;
    },
    // 获取文档完整的高度
    getScrollHeight() {
        return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    },
    getClientSize() {
        return {
            height: document.body.clientHeight,
            width: document.body.clientWidth
        }
    },

    dateFormat(tempDate) {
        if(!tempDate || isNaN(new Date(tempDate).valueOf())){
            return ''
        }

        let year = tempDate.getFullYear().toString(),
            month = (tempDate.getMonth() + 1).toString(),
            date = tempDate.getDate().toString(),
            hour = tempDate.getHours().toString(),
            minute = tempDate.getMinutes().toString(),
            second = tempDate.getSeconds().toString(),
            rst = '';

        rst = year.padStart(4, '0') +
            month.padStart(2, '0') +
            date.padStart(2, '0') +
            hour.padStart(2, '0') +
            minute.padStart(2, '0') +
            second.padStart(2, '0');

        return rst;
    }
}


export default common
