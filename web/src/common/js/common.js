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
  changeTitle:function (val){
    document.getElementsByTagName('title')[0].innerHTML = val;
    window.setDocumentTitle = function(title) {
      var i = document.createElement('iframe');
      i.src = '../favicon.ico';
      i.style.display = 'none';
      i.onload = function() {
        setTimeout(function(){
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
  getClientSize(){
    return {
      height: document.body.clientHeight,
      width: document.body.clientWidth
    }
  }
}
export default common
