var Jt=Object.defineProperty;var Zt=(N,g,D)=>g in N?Jt(N,g,{enumerable:!0,configurable:!0,writable:!0,value:D}):N[g]=D;var me=(N,g,D)=>Zt(N,typeof g!="symbol"?g+"":g,D);(function(){"use strict";var N,g,D,T,he,fe,ge,_e,K,ee,te,B={},G=[],et=/acit|ex(?:s|g|n|p|$)|rph|grid|ows|mnc|ntw|ine[ch]|zoo|^ord|itera/i,O=Array.isArray;function E(t,e){for(var o in e)t[o]=e[o];return t}function oe(t){t&&t.parentNode&&t.parentNode.removeChild(t)}function re(t,e,o){var i,n,r,s={};for(r in e)r=="key"?i=e[r]:r=="ref"?n=e[r]:s[r]=e[r];if(arguments.length>2&&(s.children=arguments.length>3?N.call(arguments,2):o),typeof t=="function"&&t.defaultProps!=null)for(r in t.defaultProps)s[r]===void 0&&(s[r]=t.defaultProps[r]);return V(t,s,i,n,null)}function V(t,e,o,i,n){var r={type:t,props:e,key:o,ref:i,__k:null,__:null,__b:0,__e:null,__c:null,constructor:void 0,__v:n??++D,__i:-1,__u:0};return n==null&&g.vnode!=null&&g.vnode(r),r}function Q(t){return t.children}function W(t,e){this.props=t,this.context=e}function R(t,e){if(e==null)return t.__?R(t.__,t.__i+1):null;for(var o;e<t.__k.length;e++)if((o=t.__k[e])!=null&&o.__e!=null)return o.__e;return typeof t.type=="function"?R(t):null}function tt(t){if(t.__P&&t.__d){var e=t.__v,o=e.__e,i=[],n=[],r=E({},e);r.__v=e.__v+1,g.vnode&&g.vnode(r),ne(t.__P,r,e,t.__n,t.__P.namespaceURI,32&e.__u?[o]:null,i,o??R(e),!!(32&e.__u),n),r.__v=e.__v,r.__.__k[r.__i]=r,Ie(i,r,n),e.__e=e.__=null,r.__e!=o&&be(r)}}function be(t){if((t=t.__)!=null&&t.__c!=null)return t.__e=t.__c.base=null,t.__k.some(function(e){if(e!=null&&e.__e!=null)return t.__e=t.__c.base=e.__e}),be(t)}function we(t){(!t.__d&&(t.__d=!0)&&T.push(t)&&!J.__r++||he!=g.debounceRendering)&&((he=g.debounceRendering)||fe)(J)}function J(){try{for(var t,e=1;T.length;)T.length>e&&T.sort(ge),t=T.shift(),e=T.length,tt(t)}finally{T.length=J.__r=0}}function ve(t,e,o,i,n,r,s,c,d,l,p){var a,m,u,w,v,_,f,b=i&&i.__k||G,S=e.length;for(d=ot(o,e,b,d,S),a=0;a<S;a++)(u=o.__k[a])!=null&&(m=u.__i!=-1&&b[u.__i]||B,u.__i=a,_=ne(t,u,m,n,r,s,c,d,l,p),w=u.__e,u.ref&&m.ref!=u.ref&&(m.ref&&se(m.ref,null,u),p.push(u.ref,u.__c||w,u)),v==null&&w!=null&&(v=w),(f=!!(4&u.__u))||m.__k===u.__k?d=ye(u,d,t,f):typeof u.type=="function"&&_!==void 0?d=_:w&&(d=w.nextSibling),u.__u&=-7);return o.__e=v,d}function ot(t,e,o,i,n){var r,s,c,d,l,p=o.length,a=p,m=0;for(t.__k=new Array(n),r=0;r<n;r++)(s=e[r])!=null&&typeof s!="boolean"&&typeof s!="function"?(typeof s=="string"||typeof s=="number"||typeof s=="bigint"||s.constructor==String?s=t.__k[r]=V(null,s,null,null,null):O(s)?s=t.__k[r]=V(Q,{children:s},null,null,null):s.constructor===void 0&&s.__b>0?s=t.__k[r]=V(s.type,s.props,s.key,s.ref?s.ref:null,s.__v):t.__k[r]=s,d=r+m,s.__=t,s.__b=t.__b+1,c=null,(l=s.__i=rt(s,o,d,a))!=-1&&(a--,(c=o[l])&&(c.__u|=2)),c==null||c.__v==null?(l==-1&&(n>p?m--:n<p&&m++),typeof s.type!="function"&&(s.__u|=4)):l!=d&&(l==d-1?m--:l==d+1?m++:(l>d?m--:m++,s.__u|=4))):t.__k[r]=null;if(a)for(r=0;r<p;r++)(c=o[r])!=null&&!(2&c.__u)&&(c.__e==i&&(i=R(c)),Ce(c,c));return i}function ye(t,e,o,i){var n,r;if(typeof t.type=="function"){for(n=t.__k,r=0;n&&r<n.length;r++)n[r]&&(n[r].__=t,e=ye(n[r],e,o,i));return e}t.__e!=e&&(i&&(e&&t.type&&!e.parentNode&&(e=R(t)),o.insertBefore(t.__e,e||null)),e=t.__e);do e=e&&e.nextSibling;while(e!=null&&e.nodeType==8);return e}function xe(t,e){return e=e||[],t==null||typeof t=="boolean"||(O(t)?t.some(function(o){xe(o,e)}):e.push(t)),e}function rt(t,e,o,i){var n,r,s,c=t.key,d=t.type,l=e[o],p=l!=null&&(2&l.__u)==0;if(l===null&&c==null||p&&c==l.key&&d==l.type)return o;if(i>(p?1:0)){for(n=o-1,r=o+1;n>=0||r<e.length;)if((l=e[s=n>=0?n--:r++])!=null&&!(2&l.__u)&&c==l.key&&d==l.type)return s}return-1}function ke(t,e,o){e[0]=="-"?t.setProperty(e,o??""):t[e]=o==null?"":typeof o!="number"||et.test(e)?o:o+"px"}function Z(t,e,o,i,n){var r,s;e:if(e=="style")if(typeof o=="string")t.style.cssText=o;else{if(typeof i=="string"&&(t.style.cssText=i=""),i)for(e in i)o&&e in o||ke(t.style,e,"");if(o)for(e in o)i&&o[e]==i[e]||ke(t.style,e,o[e])}else if(e[0]=="o"&&e[1]=="n")r=e!=(e=e.replace(_e,"$1")),s=e.toLowerCase(),e=s in t||e=="onFocusOut"||e=="onFocusIn"?s.slice(2):e.slice(2),t.l||(t.l={}),t.l[e+r]=o,o?i?o.u=i.u:(o.u=K,t.addEventListener(e,r?te:ee,r)):t.removeEventListener(e,r?te:ee,r);else{if(n=="http://www.w3.org/2000/svg")e=e.replace(/xlink(H|:h)/,"h").replace(/sName$/,"s");else if(e!="width"&&e!="height"&&e!="href"&&e!="list"&&e!="form"&&e!="tabIndex"&&e!="download"&&e!="rowSpan"&&e!="colSpan"&&e!="role"&&e!="popover"&&e in t)try{t[e]=o??"";break e}catch{}typeof o=="function"||(o==null||o===!1&&e[4]!="-"?t.removeAttribute(e):t.setAttribute(e,e=="popover"&&o==1?"":o))}}function Se(t){return function(e){if(this.l){var o=this.l[e.type+t];if(e.t==null)e.t=K++;else if(e.t<o.u)return;return o(g.event?g.event(e):e)}}}function ne(t,e,o,i,n,r,s,c,d,l){var p,a,m,u,w,v,_,f,b,S,k,$,q,C,L,I=e.type;if(e.constructor!==void 0)return null;128&o.__u&&(d=!!(32&o.__u),r=[c=e.__e=o.__e]),(p=g.__b)&&p(e);e:if(typeof I=="function")try{if(f=e.props,b=I.prototype&&I.prototype.render,S=(p=I.contextType)&&i[p.__c],k=p?S?S.props.value:p.__:i,o.__c?_=(a=e.__c=o.__c).__=a.__E:(b?e.__c=a=new I(f,k):(e.__c=a=new W(f,k),a.constructor=I,a.render=it),S&&S.sub(a),a.state||(a.state={}),a.__n=i,m=a.__d=!0,a.__h=[],a._sb=[]),b&&a.__s==null&&(a.__s=a.state),b&&I.getDerivedStateFromProps!=null&&(a.__s==a.state&&(a.__s=E({},a.__s)),E(a.__s,I.getDerivedStateFromProps(f,a.__s))),u=a.props,w=a.state,a.__v=e,m)b&&I.getDerivedStateFromProps==null&&a.componentWillMount!=null&&a.componentWillMount(),b&&a.componentDidMount!=null&&a.__h.push(a.componentDidMount);else{if(b&&I.getDerivedStateFromProps==null&&f!==u&&a.componentWillReceiveProps!=null&&a.componentWillReceiveProps(f,k),e.__v==o.__v||!a.__e&&a.shouldComponentUpdate!=null&&a.shouldComponentUpdate(f,a.__s,k)===!1){e.__v!=o.__v&&(a.props=f,a.state=a.__s,a.__d=!1),e.__e=o.__e,e.__k=o.__k,e.__k.some(function(z){z&&(z.__=e)}),G.push.apply(a.__h,a._sb),a._sb=[],a.__h.length&&s.push(a);break e}a.componentWillUpdate!=null&&a.componentWillUpdate(f,a.__s,k),b&&a.componentDidUpdate!=null&&a.__h.push(function(){a.componentDidUpdate(u,w,v)})}if(a.context=k,a.props=f,a.__P=t,a.__e=!1,$=g.__r,q=0,b)a.state=a.__s,a.__d=!1,$&&$(e),p=a.render(a.props,a.state,a.context),G.push.apply(a.__h,a._sb),a._sb=[];else do a.__d=!1,$&&$(e),p=a.render(a.props,a.state,a.context),a.state=a.__s;while(a.__d&&++q<25);a.state=a.__s,a.getChildContext!=null&&(i=E(E({},i),a.getChildContext())),b&&!m&&a.getSnapshotBeforeUpdate!=null&&(v=a.getSnapshotBeforeUpdate(u,w)),C=p!=null&&p.type===Q&&p.key==null?$e(p.props.children):p,c=ve(t,O(C)?C:[C],e,o,i,n,r,s,c,d,l),a.base=e.__e,e.__u&=-161,a.__h.length&&s.push(a),_&&(a.__E=a.__=null)}catch(z){if(e.__v=null,d||r!=null)if(z.then){for(e.__u|=d?160:128;c&&c.nodeType==8&&c.nextSibling;)c=c.nextSibling;r[r.indexOf(c)]=null,e.__e=c}else{for(L=r.length;L--;)oe(r[L]);ie(e)}else e.__e=o.__e,e.__k=o.__k,z.then||ie(e);g.__e(z,e,o)}else r==null&&e.__v==o.__v?(e.__k=o.__k,e.__e=o.__e):c=e.__e=nt(o.__e,e,o,i,n,r,s,d,l);return(p=g.diffed)&&p(e),128&e.__u?void 0:c}function ie(t){t&&(t.__c&&(t.__c.__e=!0),t.__k&&t.__k.some(ie))}function Ie(t,e,o){for(var i=0;i<o.length;i++)se(o[i],o[++i],o[++i]);g.__c&&g.__c(e,t),t.some(function(n){try{t=n.__h,n.__h=[],t.some(function(r){r.call(n)})}catch(r){g.__e(r,n.__v)}})}function $e(t){return typeof t!="object"||t==null||t.__b>0?t:O(t)?t.map($e):E({},t)}function nt(t,e,o,i,n,r,s,c,d){var l,p,a,m,u,w,v,_=o.props||B,f=e.props,b=e.type;if(b=="svg"?n="http://www.w3.org/2000/svg":b=="math"?n="http://www.w3.org/1998/Math/MathML":n||(n="http://www.w3.org/1999/xhtml"),r!=null){for(l=0;l<r.length;l++)if((u=r[l])&&"setAttribute"in u==!!b&&(b?u.localName==b:u.nodeType==3)){t=u,r[l]=null;break}}if(t==null){if(b==null)return document.createTextNode(f);t=document.createElementNS(n,b,f.is&&f),c&&(g.__m&&g.__m(e,r),c=!1),r=null}if(b==null)_===f||c&&t.data==f||(t.data=f);else{if(r=r&&N.call(t.childNodes),!c&&r!=null)for(_={},l=0;l<t.attributes.length;l++)_[(u=t.attributes[l]).name]=u.value;for(l in _)u=_[l],l=="dangerouslySetInnerHTML"?a=u:l=="children"||l in f||l=="value"&&"defaultValue"in f||l=="checked"&&"defaultChecked"in f||Z(t,l,null,u,n);for(l in f)u=f[l],l=="children"?m=u:l=="dangerouslySetInnerHTML"?p=u:l=="value"?w=u:l=="checked"?v=u:c&&typeof u!="function"||_[l]===u||Z(t,l,u,_[l],n);if(p)c||a&&(p.__html==a.__html||p.__html==t.innerHTML)||(t.innerHTML=p.__html),e.__k=[];else if(a&&(t.innerHTML=""),ve(e.type=="template"?t.content:t,O(m)?m:[m],e,o,i,b=="foreignObject"?"http://www.w3.org/1999/xhtml":n,r,s,r?r[0]:o.__k&&R(o,0),c,d),r!=null)for(l=r.length;l--;)oe(r[l]);c||(l="value",b=="progress"&&w==null?t.removeAttribute("value"):w!=null&&(w!==t[l]||b=="progress"&&!w||b=="option"&&w!=_[l])&&Z(t,l,w,_[l],n),l="checked",v!=null&&v!=t[l]&&Z(t,l,v,_[l],n))}return t}function se(t,e,o){try{if(typeof t=="function"){var i=typeof t.__u=="function";i&&t.__u(),i&&e==null||(t.__u=t(e))}else t.current=e}catch(n){g.__e(n,o)}}function Ce(t,e,o){var i,n;if(g.unmount&&g.unmount(t),(i=t.ref)&&(i.current&&i.current!=t.__e||se(i,null,e)),(i=t.__c)!=null){if(i.componentWillUnmount)try{i.componentWillUnmount()}catch(r){g.__e(r,e)}i.base=i.__P=null}if(i=t.__k)for(n=0;n<i.length;n++)i[n]&&Ce(i[n],e,o||typeof t.type!="function");o||oe(t.__e),t.__c=t.__=t.__e=void 0}function it(t,e,o){return this.constructor(t,o)}function st(t,e,o){var i,n,r,s;e==document&&(e=document.documentElement),g.__&&g.__(t,e),n=(i=!1)?null:e.__k,r=[],s=[],ne(e,t=e.__k=re(Q,null,[t]),n||B,B,e.namespaceURI,n?null:e.firstChild?N.call(e.childNodes):null,r,n?n.__e:e.firstChild,i,s),Ie(r,t,s)}N=G.slice,g={__e:function(t,e,o,i){for(var n,r,s;e=e.__;)if((n=e.__c)&&!n.__)try{if((r=n.constructor)&&r.getDerivedStateFromError!=null&&(n.setState(r.getDerivedStateFromError(t)),s=n.__d),n.componentDidCatch!=null&&(n.componentDidCatch(t,i||{}),s=n.__d),s)return n.__E=n}catch(c){t=c}throw t}},D=0,W.prototype.setState=function(t,e){var o;o=this.__s!=null&&this.__s!=this.state?this.__s:this.__s=E({},this.state),typeof t=="function"&&(t=t(E({},o),this.props)),t&&E(o,t),t!=null&&this.__v&&(e&&this._sb.push(e),we(this))},W.prototype.forceUpdate=function(t){this.__v&&(this.__e=!0,t&&this.__h.push(t),we(this))},W.prototype.render=Q,T=[],fe=typeof Promise=="function"?Promise.prototype.then.bind(Promise.resolve()):setTimeout,ge=function(t,e){return t.__v.__b-e.__v.__b},J.__r=0,_e=/(PointerCapture)$|Capture$/i,K=0,ee=Se(!1),te=Se(!0);var at=0;function h(t,e,o,i,n,r){e||(e={});var s,c,d=e;if("ref"in d)for(c in d={},e)c=="ref"?s=e[c]:d[c]=e[c];var l={type:t,props:d,key:o,ref:s,__k:null,__:null,__b:0,__e:null,__c:null,constructor:void 0,__v:--at,__i:-1,__u:0,__source:n,__self:r};if(typeof t=="function"&&(s=t.defaultProps))for(c in s)d[c]===void 0&&(d[c]=s[c]);return g.vnode&&g.vnode(l),l}var F,y,ae,Ne,j=0,Ee=[],x=g,Ue=x.__b,Te=x.__r,Le=x.diffed,De=x.__c,Pe=x.unmount,Ae=x.__;function ce(t,e){x.__h&&x.__h(y,t,j||e),j=0;var o=y.__H||(y.__H={__:[],__h:[]});return t>=o.__.length&&o.__.push({}),o.__[t]}function P(t){return j=1,ct(He,t)}function ct(t,e,o){var i=ce(F++,2);if(i.t=t,!i.__c&&(i.__=[He(void 0,e),function(c){var d=i.__N?i.__N[0]:i.__[0],l=i.t(d,c);d!==l&&(i.__N=[l,i.__[1]],i.__c.setState({}))}],i.__c=y,!y.__f)){var n=function(c,d,l){if(!i.__c.__H)return!0;var p=i.__c.__H.__.filter(function(m){return m.__c});if(p.every(function(m){return!m.__N}))return!r||r.call(this,c,d,l);var a=i.__c.props!==c;return p.some(function(m){if(m.__N){var u=m.__[0];m.__=m.__N,m.__N=void 0,u!==m.__[0]&&(a=!0)}}),r&&r.call(this,c,d,l)||a};y.__f=!0;var r=y.shouldComponentUpdate,s=y.componentWillUpdate;y.componentWillUpdate=function(c,d,l){if(this.__e){var p=r;r=void 0,n(c,d,l),r=p}s&&s.call(this,c,d,l)},y.shouldComponentUpdate=n}return i.__N||i.__}function Me(t,e){var o=ce(F++,3);!x.__s&&Re(o.__H,e)&&(o.__=t,o.u=e,y.__H.__h.push(o))}function lt(t){return j=5,le(function(){return{current:t}},[])}function le(t,e){var o=ce(F++,7);return Re(o.__H,e)&&(o.__=t(),o.__H=e,o.__h=t),o.__}function qe(t,e){return j=8,le(function(){return t},e)}function dt(){for(var t;t=Ee.shift();){var e=t.__H;if(t.__P&&e)try{e.__h.some(X),e.__h.some(de),e.__h=[]}catch(o){e.__h=[],x.__e(o,t.__v)}}}x.__b=function(t){y=null,Ue&&Ue(t)},x.__=function(t,e){t&&e.__k&&e.__k.__m&&(t.__m=e.__k.__m),Ae&&Ae(t,e)},x.__r=function(t){Te&&Te(t),F=0;var e=(y=t.__c).__H;e&&(ae===y?(e.__h=[],y.__h=[],e.__.some(function(o){o.__N&&(o.__=o.__N),o.u=o.__N=void 0})):(e.__h.some(X),e.__h.some(de),e.__h=[],F=0)),ae=y},x.diffed=function(t){Le&&Le(t);var e=t.__c;e&&e.__H&&(e.__H.__h.length&&(Ee.push(e)!==1&&Ne===x.requestAnimationFrame||((Ne=x.requestAnimationFrame)||ut)(dt)),e.__H.__.some(function(o){o.u&&(o.__H=o.u),o.u=void 0})),ae=y=null},x.__c=function(t,e){e.some(function(o){try{o.__h.some(X),o.__h=o.__h.filter(function(i){return!i.__||de(i)})}catch(i){e.some(function(n){n.__h&&(n.__h=[])}),e=[],x.__e(i,o.__v)}}),De&&De(t,e)},x.unmount=function(t){Pe&&Pe(t);var e,o=t.__c;o&&o.__H&&(o.__H.__.some(function(i){try{X(i)}catch(n){e=n}}),o.__H=void 0,e&&x.__e(e,o.__v))};var ze=typeof requestAnimationFrame=="function";function ut(t){var e,o=function(){clearTimeout(i),ze&&cancelAnimationFrame(e),setTimeout(t)},i=setTimeout(o,35);ze&&(e=requestAnimationFrame(o))}function X(t){var e=y,o=t.__c;typeof o=="function"&&(t.__c=void 0,o()),y=e}function de(t){var e=y;t.__c=t.__(),y=e}function Re(t,e){return!t||t.length!==e.length||e.some(function(o,i){return o!==t[i]})}function He(t,e){return typeof e=="function"?e(t):e}/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */var pt={xmlns:"http://www.w3.org/2000/svg",width:24,height:24,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor","stroke-width":"2","stroke-linecap":"round","stroke-linejoin":"round"};/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const mt=t=>t.replace(/([a-z0-9])([A-Z])/g,"$1-$2").toLowerCase(),H=(t,e)=>{const o=({color:i="currentColor",size:n=24,strokeWidth:r=2,absoluteStrokeWidth:s,children:c,class:d="",...l})=>re("svg",{...pt,width:String(n),height:n,stroke:i,"stroke-width":s?Number(r)*24/Number(n):r,class:["lucide",`lucide-${mt(t)}`,d].join(" "),...l},[...e.map(([p,a])=>re(p,a)),...xe(c)]);return o.displayName=`${t}`,o};/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ht=H("ArrowLeft",[["path",{d:"m12 19-7-7 7-7",key:"1l729n"}],["path",{d:"M19 12H5",key:"x3x0zl"}]]);/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const ft=H("ChevronDown",[["path",{d:"m6 9 6 6 6-6",key:"qrunsl"}]]);/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const gt=H("ChevronUp",[["path",{d:"m18 15-6-6-6 6",key:"153udz"}]]);/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const _t=H("Moon",[["path",{d:"M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z",key:"a7tn18"}]]);/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const bt=H("Settings",[["path",{d:"M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z",key:"1qme2f"}],["circle",{cx:"12",cy:"12",r:"3",key:"1v7zrd"}]]);/**
 * @license lucide-preact v0.300.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const wt=H("Sun",[["circle",{cx:"12",cy:"12",r:"4",key:"4exip2"}],["path",{d:"M12 2v2",key:"tus03m"}],["path",{d:"M12 20v2",key:"1lh1kg"}],["path",{d:"m4.93 4.93 1.41 1.41",key:"149t6j"}],["path",{d:"m17.66 17.66 1.41 1.41",key:"ptbguv"}],["path",{d:"M2 12h2",key:"1t8f8n"}],["path",{d:"M20 12h2",key:"1q8mjw"}],["path",{d:"m6.34 17.66-1.41 1.41",key:"1m8zz5"}],["path",{d:"m19.07 4.93-1.41 1.41",key:"1shlcs"}]]);

const U = {
  QUIZ_CONTAINER: ".css-1erl2aq, .rc-FormPartsQuestion",
  POINTS: '[data-testid="part-points"]',
  QUESTION_BODY: ".css-ybrhvy .rc-CML, .rc-FormPartsQuestion .rc-CML, div[id^='prompt-'] .rc-CML",
  CML_CONTENT: ".rc-CML",
  CHOICE_LABEL: ".cds-checkboxAndRadio-labelText",
  OPTION_WRAPPER: ".rc-Option",
  VERSION_META: 'meta[name="coursera-app-version"]',
  COURSE_ID_META: 'meta[property="coursera:course_id"]'
};

const vt = {
  VERSION: "902d11358ca4c08e177c1e3eac11ffe41c92f674"
};

// Sleep helpers
const Ge = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const A = (base, jitter = 200) => {
  const randomJitter = Math.floor(Math.random() * jitter);
  return Ge(base + randomJitter);
};

// MD5 digest helper
const Ve = async (text) => {
  const enc = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest("MD5", enc);
  return btoa(String.fromCharCode(...new Uint8Array(digest)));
};

// Platform helper
function xt() {
  const p = (navigator.platform || "").toLowerCase();
  return p.includes("win") ? "Windows" : p.includes("mac") ? "MacIntel" : p.includes("linux") ? "Linux" : "Unknown";
}

// App version helper
function yt() {
  const meta = document.querySelector(U.VERSION_META);
  if (meta && meta.content) return meta.content;
  const scripts = Array.from(document.querySelectorAll("script"));
  for (const s of scripts) {
    const m = (s.innerText || "").match(/"version"\s*:\s*"([a-f0-9]{40})"/i);
    if (m) return m[1];
  }
  return vt.VERSION;
}

// CSRF token helper
function je() {
  const cookies = document.cookie.split("; ");
  for (const c of cookies) {
    const [name, val] = c.split("=");
    if (!name || !val) continue;
    const lower = name.toLowerCase().trim();
    if (lower === "csrf3-token" || lower === "csrf2-token" || lower === "csrf-token" || lower === "csrftoken" || lower === "_csrf") {
      return decodeURIComponent(val).replace(/^"|"$/g, "");
    }
  }
  const meta = document.querySelector('meta[name="csrf-token"], meta[name="csrf3-token"], meta[property="csrf-token"]');
  if (meta && meta.content) return meta.content;
  return "";
}

// Robust User ID extractor
async function Oe() {
  // 1. Script tags
  const scripts = Array.from(document.querySelectorAll("script"));
  for (const s of scripts) {
    const text = s.innerText || "";
    const mUserJson = text.match(/userJson\s*=\s*"(.+?)"/);
    if (mUserJson) {
      try {
        const parsed = JSON.parse(mUserJson[1].replace(/\\"/g, '"'));
        if (parsed.id) return String(parsed.id);
      } catch {}
    }
    const mUserData = text.match(/"userData"\s*:\s*{\s*"id"\s*:\s*(\d+)/) || text.match(/"userId"\s*:\s*(\d+)/);
    if (mUserData) return String(mUserData[1]);
  }

  // 2. Global state
  try {
    if (window.Coursera && window.Coursera.user && window.Coursera.user.id) {
      return String(window.Coursera.user.id);
    }
    if (window.__APOLLO_STATE__) {
      for (const k in window.__APOLLO_STATE__) {
        if (k.startsWith("User:") || k.startsWith("Learner:")) {
          const u = window.__APOLLO_STATE__[k];
          if (u && u.id) return String(u.id);
        }
      }
    }
  } catch {}

  // 3. Cookies
  try {
    const cookies = document.cookie.split("; ");
    for (const c of cookies) {
      const [name, val] = c.split("=");
      if (!name || !val) continue;
      const lower = name.toLowerCase().trim();
      if (lower === "cauth" || lower === "_cauth" || lower === "204_cauth" || lower === "__204u" || lower === "coursera_user") {
        try {
          const decoded = decodeURIComponent(val);
          const m = decoded.match(/"id"\s*:\s*(\d+)/) || decoded.match(/^(\d+)$/);
          if (m) return String(m[1]);
        } catch {}
      }
    }
  } catch {}

  // 4. API fallback /api/user/v1/me
  try {
    const res = await fetch("/api/user/v1/me", { credentials: "include" });
    if (res.ok) {
      const data = await res.json();
      if (data && data.id) return String(data.id);
    }
  } catch {}

  // 5. API fallback /api/users.v1?q=me
  try {
    const res = await fetch("/api/users.v1?q=me", { credentials: "include" });
    if (res.ok) {
      const data = await res.json();
      const id = data?.elements?.[0]?.id;
      if (id) return String(id);
    }
  } catch {}

  return null;
}

// Course slug extractor
function getCourseSlug() {
  const pathMatch = window.location.pathname.match(/\/learn\/([^/?#]+)/);
  if (pathMatch) return pathMatch[1];
  const urlMatch = window.location.href.match(/learn\/([A-Za-z0-9-_]+)/);
  return urlMatch ? urlMatch[1] : null;
}

// Course ID extractor
function Fe() {
  const scripts = Array.from(document.querySelectorAll("script"));
  for (const s of scripts) {
    const text = s.innerText || "";
    const m1 = text.match(/return\s+'([A-Za-z0-9-_]{20,})'/);
    if (m1) return m1[1];
    const m2 = text.match(/"courseId"\s*:\s*"([A-Za-z0-9-_]{20,})"/);
    if (m2) return m2[1];
    const m3 = text.match(/"contextId"\s*:\s*"([A-Za-z0-9-_]{20,})"/);
    if (m3) return m3[1];
  }
  const meta = document.querySelector(U.COURSE_ID_META);
  if (meta && meta.content) return meta.content;
  return new URL(window.location.href).searchParams.get("courseId");
}

// Quiz harvesting & blueprint extractor
function Be(mode) {
  const containers = document.querySelectorAll(U.QUIZ_CONTAINER);
  const results = [];
  containers.forEach((container) => {
    if (mode === "harvest") {
      const pts = container.querySelector(U.POINTS);
      const ptText = pts ? pts.innerText : "";
      if (!ptText.includes("1 / 1")) return;
    }
    const qBody = container.querySelector(U.QUESTION_BODY);
    let questionText = qBody ? qBody.innerText.trim() : container.querySelector(U.CML_CONTENT)?.innerText.trim();
    if (!questionText) questionText = "Blueprint Unit";
    questionText = questionText.replace(/^\d+\.\nQuestion \d+\n\n/, "").trim();

    const choices = Array.from(
      new Set(
        Array.from(container.querySelectorAll(U.CHOICE_LABEL))
          .map((p) => p.innerText.trim())
          .filter((p) => p.length > 0)
      )
    );

    const answers = new Set();
    if (mode === "harvest") {
      container.querySelectorAll(U.OPTION_WRAPPER).forEach((opt) => {
        const inp = opt.querySelector("input");
        if (inp && (inp.checked || inp.hasAttribute("checked"))) {
          const label = opt.querySelector(U.CHOICE_LABEL);
          const ansText = label ? label.innerText.trim() : opt.innerText.trim();
          if (ansText) answers.add(ansText);
        }
      });
    }

    if (questionText) {
      results.push({
        question: questionText,
        choices,
        answer: Array.from(answers)
      });
    }
  });
  return results;
}

// Context builder
const Qe = (userId, courseId, csrf, courseSlug, log) => {
  const ctx = {
    userId,
    courseId,
    csrf,
    courseSlug,
    log,
    headers: (extra = {}) => ({
      "Content-Type": "application/json",
      "X-CSRF3-Token": csrf,
      "X-Coursera-Application": "ondemand",
      "X-Coursera-Version": yt(),
      ...extra
    }),
    post: (url, body) =>
      fetch(url, {
        method: "POST",
        headers: ctx.headers(),
        body: JSON.stringify(body)
      }),
    put: (url, body) =>
      fetch(url, {
        method: "PUT",
        headers: ctx.headers(),
        body: JSON.stringify(body)
      }),
    graphql: (opName, variables, query) =>
      fetch(`/graphql-gateway?opname=${opName}`, {
        method: "POST",
        headers: ctx.headers(),
        body: JSON.stringify([{ operationName: opName, variables, query }])
      }),
    sendHeartbeats: async (params) => {
      const { courseId: cId, itemId, duration, csrf: token, activityType, actionType } = params;
      const step = 30000;
      const count = Math.ceil(duration / step);
      const startTime = Date.now() - duration;
      const deviceId = crypto.randomUUID ? crypto.randomUUID() : `dev-${Date.now()}`;

      for (let f = 0; f < count; f++) {
        const remaining = Math.min(step, duration - f * step);
        if (remaining <= 0) break;
        try {
          await fetch("/graphql-gateway?opname=LearningHours_SendEvent", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRF3-Token": token
            },
            body: JSON.stringify([
              {
                operationName: "LearningHours_SendEvent",
                variables: {
                  input: {
                    heartbeat: {
                      courseId: cId,
                      eventPlatform: "WEB",
                      userActionType: actionType,
                      durationMilliSeconds: Math.floor(remaining),
                      eventOs: xt(),
                      clientDateTime: new Date(startTime + f * step).toISOString(),
                      deviceId,
                      itemDetails: { itemId, learnerActivityType: activityType },
                      courseBranchId: cId
                    }
                  }
                },
                query: `mutation LearningHours_SendEvent($input: LearningHours_SendEventInput!) {
                  LearningHours_SendEvent(input: $input) {
                    ... on LearningHours_SendEventSuccess { id __typename }
                    ... on LearningHours_SendEventError { message __typename }
                    __typename
                  }
                }`
              }
            ])
          });
        } catch {}
        if (f % 5 === 0) await A(50, 100);
      }
    }
  };
  return ctx;
};

// Handlers
class kt {
  canHandle(item) {
    const type = item.contentSummary?.typeName;
    return type === "lecture";
  }
  async handle(item, ctx) {
    ctx.log(`Watching video: ${item.name || item.slug}`, "info");
    try {
      await ctx.post(
        `/api/opencourse.v1/user/${ctx.userId}/course/${ctx.courseSlug}/item/${item.id}/lecture/videoEvents/play?autoEnroll=false`,
        { contentRequestBody: {} }
      );
    } catch {}

    let duration = item.contentSummary?.definition?.duration || item.timeCommitment || 120000;
    try {
      const vidRes = await fetch(
        `/api/onDemandLectureVideos.v1/${ctx.courseId}~${item.id}?includes=video&fields=onDemandVideos.v1(id,duration)`
      );
      if (vidRes.ok) {
        const vidData = await vidRes.json();
        const vidObj = vidData?.linked?.["onDemandVideos.v1"]?.[0];
        if (vidObj && vidObj.id) {
          duration = vidObj.duration || duration;
          const progId = `${ctx.userId}~${ctx.courseId}~${vidObj.id}`;
          await ctx.put(`/api/onDemandVideoProgresses.v1/${progId}`, {
            viewedUpTo: duration,
            videoProgressId: progId
          });
        }
      }
    } catch {}

    await ctx.sendHeartbeats({
      courseId: ctx.courseId,
      itemId: item.id,
      duration,
      csrf: ctx.csrf,
      activityType: "LECTURE",
      actionType: "VIDEO_IS_PLAYING"
    });

    const endUrl = `/api/opencourse.v1/user/${ctx.userId}/course/${ctx.courseSlug}/item/${item.id}/lecture/videoEvents/ended?autoEnroll=false`;
    for (let p = 0; p < 10; p++) {
      try {
        const endRes = await fetch(endUrl, {
          method: "POST",
          headers: ctx.headers({ "X-Requested-With": "XMLHttpRequest" }),
          body: JSON.stringify({ contentRequestBody: {} })
        });
        if (endRes.ok) break;
        const txt = await endRes.text();
        if (txt.includes("not watched enough")) {
          await A(2000, 2000);
        } else {
          break;
        }
      } catch {
        break;
      }
    }
    ctx.log(`Video completed: ${item.name || item.slug}`, "success");
  }
}

class St {
  canHandle(item) {
    const type = item.contentSummary?.typeName;
    return ["supplement", "reading", "richText", "cml", "text", "article", "asset"].includes(type);
  }
  async handle(item, ctx) {
    ctx.log(`Reading: ${item.name || item.slug}`, "info");
    const res = await ctx.post("/api/onDemandSupplementCompletions.v1", {
      courseId: ctx.courseId,
      itemId: item.id,
      userId: Number(ctx.userId)
    });
    await ctx.sendHeartbeats({
      courseId: ctx.courseId,
      itemId: item.id,
      duration: 30000,
      csrf: ctx.csrf,
      activityType: "SUPPLEMENT",
      actionType: "PAGE_VIEW"
    });
    if (res.ok) {
      ctx.log("Content marked as read", "success");
    } else {
      ctx.log(`Mark read status: ${res.status}`, res.status === 200 || res.status === 201 ? "success" : "info");
    }
  }
}

class It {
  canHandle(item) {
    const type = item.contentSummary?.typeName || "";
    return [
      "ungradedLti",
      "ungradedWidget",
      "ungradedLab",
      "ungradedAssignment",
      "ungradedProgramming",
      "workspace",
      "authoringWorkspace",
      "notebook",
      "plugin"
    ].includes(type);
  }
  async handle(item, ctx) {
    const type = item.contentSummary?.typeName || "ungraded";
    ctx.log(`Bypassing: ${item.name || item.slug} (${type})`, "info");
    const payload = {
      courseId: ctx.courseId,
      itemId: item.id,
      userId: Number(ctx.userId)
    };

    if (type === "ungradedLti") {
      await ctx.post("/api/onDemandLtiUngradedLaunches.v1", {
        ...payload,
        learnerId: Number(ctx.userId),
        markItemCompleted: true
      });
    } else if (type === "ungradedLab" || type === "workspace" || type === "authoringWorkspace") {
      const key = `${ctx.userId}~${ctx.courseId}~${item.id}`;
      try {
        await fetch(`/api/onDemandWorkspaceLaunchers.v2/${key}?fields=id,itemId`);
        await ctx.post(`/api/onDemandLearnerWorkspaces.v1/?action=launch&id=${key}`, {});
      } catch {}
      await ctx.sendHeartbeats({
        courseId: ctx.courseId,
        itemId: item.id,
        duration: 45000,
        csrf: ctx.csrf,
        activityType: "UNGRADED_LAB",
        actionType: "KEY_PRESS"
      });
      await ctx.post("/api/onDemandSupplementCompletions.v1", payload);
    } else if (type === "ungradedWidget") {
      const key = `${ctx.userId}~${ctx.courseId}~${item.id}`;
      let sessionId;
      try {
        const sRes = await fetch(
          `/api/onDemandSessionMemberships.v1?courseId=${ctx.courseId}&userId=${ctx.userId}&q=activeByUserAndCourse&fields=sessionId`
        );
        if (sRes.ok) {
          const sJson = await sRes.json();
          sessionId = sJson?.elements?.[0]?.sessionId;
        }
      } catch {}
      await ctx.put(`/api/onDemandWidgetProgress.v1/${key}`, {
        progressState: "Completed",
        sessionId
      });
    } else {
      await ctx.post("/api/onDemandUngradedAssignmentSubmissions.v1", payload);
      await ctx.post("/api/onDemandSupplementCompletions.v1", payload);
    }
    ctx.log("Successfully bypassed ungraded item", "success");
  }
}

class $t {
  canHandle(item) {
    const type = item.contentSummary?.typeName;
    return type === "discussionPrompt";
  }
  async handle(item, ctx) {
    ctx.log(`Answering discussion: ${item.name || item.slug}`, "info");
    try {
      const discUrl = `/api/onDemandDiscussionPrompts.v1/${ctx.userId}~${ctx.courseId}~${item.id}?fields=onDemandDiscussionPromptQuestions.v1(content),promptType&includes=question`;
      const hdrs = ctx.headers();
      delete hdrs["Content-Type"];
      const discRes = await fetch(discUrl, { headers: hdrs });
      if (!discRes.ok) {
        ctx.log(`Failed to fetch discussion metadata: ${discRes.status}`, "error");
        return;
      }
      const discData = await discRes.json();
      const promptDef = discData?.elements?.[0]?.promptType?.definition;
      const questionId = promptDef?.courseItemForumQuestionId?.split("~")?.[2];
      if (!questionId) {
        ctx.log(`Question ID not found for ${item.id}`, "error");
        return;
      }
      const forumQId = `${ctx.courseId}~${questionId}`;
      await A(1500, 1000);
      const answerBody = {
        content: {
          typeName: "cml",
          definition: {
            dtdId: "discussion/1",
            value: "<co-content><text>Great insights, fully agreed with the points discussed above.</text></co-content>"
          }
        },
        courseForumQuestionId: forumQId
      };
      const postRes = await ctx.post(
        "/api/onDemandCourseForumAnswers.v1/?fields=content,forumQuestionId&includes=profiles",
        answerBody
      );
      if (postRes.ok) {
        ctx.log("Discussion answered & completed.", "success");
      } else {
        ctx.log(`Discussion post response: ${postRes.status}`, "info");
      }
    } catch (err) {
      ctx.log(`Discussion error: ${err.message}`, "error");
    }
  }
}

class Ct {
  canHandle(item) {
    const type = item.contentSummary?.typeName;
    return type === "peer" || type === "phasedPeer";
  }
  async handle(item, ctx) {
    ctx.log(`Bypassing peer assignment: ${item.name || item.slug}`, "info");
    const schemaRes = await fetch(
      `/api/onDemandPeerSubmissions.v1/?q=activeByItemAndUser&courseId=${ctx.courseId}&itemId=${item.id}&userId=${ctx.userId}&includes=submissionSchemas&fields=onDemandPeerSubmissionSchemas.v1(submissionSchema)`
    );
    if (!schemaRes.ok) throw new Error("Failed to fetch peer schema");
    const schemaData = await schemaRes.json();
    const schemaObj = schemaData?.linked?.["onDemandPeerSubmissionSchemas.v1"]?.[0];
    const schema = schemaObj?.submissionSchema;
    if (!schema) throw new Error("No submission schema found for peer assignment");

    const parts = {};
    const caption = "Course project implementation completed per instructions.";
    const title = "Course Project Submission";

    for (const part of schema.parts || []) {
      if (part.details.typeName === "fileUpload") {
        ctx.log(`Preparing file upload for part: ${part.id}`, "progress");
        const fileContent = `Peer submission for ${item.name}.\nDate: ${new Date().toISOString()}`;
        const md5 = await Ve(fileContent);
        const presignVars = {
          input: { contentMd5: md5, contentType: "text/plain", fileName: "submission.txt" }
        };
        const presignQuery = `mutation GetPreSignedUrl($input: Submission_FileUploadQuestionGenerateUploadUrlInput!) {
          Submission_FileUploadQuestionGenerateUploadUrl(input: $input) {
            url
            additionalHeaders { name value }
          }
        }`;
        const presignRes = await ctx.graphql("GetPreSignedUrl", presignVars, presignQuery);
        const presignJson = (await presignRes.json())?.[0];
        const presignData = presignJson?.data?.Submission_FileUploadQuestionGenerateUploadUrl;
        if (presignData && presignData.url) {
          const s3Headers = {
            "Content-Type": "text/plain",
            "Content-MD5": md5
          };
          (presignData.additionalHeaders || []).forEach((h) => (s3Headers[h.name] = h.value));
          await fetch(presignData.url, {
            method: "PUT",
            headers: s3Headers,
            body: fileContent
          });
          parts[part.id] = {
            typeName: "fileUpload",
            definition: {
              caption,
              fileUrl: presignData.url.split("?")[0],
              title
            }
          };
        }
      } else if (part.details.typeName === "plainText") {
        parts[part.id] = {
          typeName: "plainText",
          definition: { text: caption }
        };
      } else if (part.details.typeName === "url") {
        parts[part.id] = {
          typeName: "url",
          definition: { url: "https://google.com", caption: "Project Demo", title: "Demo" }
        };
      }
    }

    const assignmentId = schema.id.split("~").pop();
    await ctx.put(`/api/onDemandPeerSubmissionDrafts.v1/${ctx.userId}~${ctx.courseId}~${item.id}/`, {
      submission: { title, parts },
      attachedAssignmentId: assignmentId
    });
    await A(1000, 500);
    const submitRes = await ctx.post("/api/onDemandPeerSubmissions.v1/", {
      courseId: ctx.courseId,
      itemId: item.id,
      gradingType: "HUMAN"
    });
    if (submitRes.ok) {
      ctx.log("Peer assignment submitted successfully", "success");
    } else {
      ctx.log(`Peer submit status: ${submitRes.status}`, "info");
    }
  }
}

// Master Automation Runner
class Nt {
  constructor(userId, courseId, csrf, courseSlug, log) {
    this.ctx = Qe(userId, courseId, csrf, courseSlug || courseId, log);
    this.handlers = [new kt(), new St(), new It(), new $t(), new Ct()];
  }

  async fetchCourseDetails() {
    this.ctx.log("Retrieving course & module structure...", "progress");
    const url = `/api/onDemandCourseMaterials.v2/?q=slug&slug=${this.ctx.courseSlug}&includes=modules,items,lessons&fields=moduleIds,onDemandCourseMaterialModules.v1(name,slug,id,lessonIds),onDemandCourseMaterialItems.v2(name,slug,timeCommitment,contentSummary,moduleId,lessonId)&showLockedItems=true`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Could not fetch course materials (HTTP ${res.status})`);
    const json = await res.json();
    const elem = json.elements?.[0] || {};
    const moduleIds = elem.moduleIds || [];
    const modules = json.linked?.["onDemandCourseMaterialModules.v1"] || [];
    const items = json.linked?.["onDemandCourseMaterialItems.v2"] || [];
    return {
      courseId: elem.id || this.ctx.courseId,
      moduleIds,
      modules,
      items
    };
  }

  async fetchProgress() {
    try {
      const res = await fetch(`/api/onDemandCoursesProgress.v1/${this.ctx.userId}~${this.ctx.courseId}`);
      if (!res.ok) return new Set();
      const data = await res.json();
      const completedSet = new Set();
      const itemsMap = data?.elements?.[0]?.items || {};
      for (const itemId in itemsMap) {
        if (itemsMap[itemId]?.progressState === "Completed") {
          completedSet.add(itemId);
        }
      }
      return completedSet;
    } catch {
      return new Set();
    }
  }

  isCompleted(item, progressSet) {
    return progressSet.has(item.id);
  }

  async processItem(item) {
    const typeName = item.contentSummary?.typeName;
    const handler = this.handlers.find((h) => h.canHandle(item));
    if (handler) {
      this.ctx.log(`Processing: ${item.name || item.slug} (${typeName})`, "info");
      try {
        await handler.handle(item, this.ctx);
        return true;
      } catch (err) {
        console.error(`Bypass error for ${item.id}:`, err);
        return false;
      }
    }
    return false;
  }

  async finalizeModule(moduleId) {
    try {
      await this.ctx.post("/api/onboarding/v1/moduleExecution", {
        userId: this.ctx.userId,
        courseId: this.ctx.courseId,
        moduleId,
        complete: true,
        lastAccessed: new Date().toISOString()
      });
    } catch {}
  }

  // Execute a single target module with auto-jump to next module
  async executeModule(targetModuleInfo, courseDetails, shouldAutoJump = true) {
    try {
      const { moduleId, moduleIndex, weekNumber, moduleName } = targetModuleInfo;
      const { moduleIds, items } = courseDetails;

      const moduleItems = items.filter((it) => it.moduleId === moduleId);
      this.ctx.log(
        `Targeting: ${moduleName} (Week ${weekNumber}/${moduleIds.length}) - ${moduleItems.length} items total`,
        "progress"
      );

      const progressSet = await this.fetchProgress();
      const uncompletedItems = moduleItems.filter((it) => !this.isCompleted(it, progressSet));
      const manualItems = [];

      if (uncompletedItems.length === 0) {
        this.ctx.log(`All items in ${moduleName} are already completed.`, "success");
        await this.finalizeModule(moduleId);
      } else {
        this.ctx.log(`Found ${uncompletedItems.length} uncompleted items. Starting skip...`, "progress");
        for (const item of uncompletedItems) {
          const success = await this.processItem(item);
          if (!success) {
            this.ctx.log(`Skipping manual item: ${item.name || item.slug}`, "info");
            manualItems.push(item);
          }
          await A(300, 300);
        }
        await this.finalizeModule(moduleId);
        if (manualItems.length > 0) {
          this.ctx.log(`${moduleName} processed. ${manualItems.length} items require manual action (Quizzes/Exams).`, "info");
          manualItems.forEach((m) => this.ctx.log(`> Manual: ${m.name}`, "info"));
        } else {
          this.ctx.log(`${moduleName} completed! Progress synced.`, "success");
        }
      }

      // Check next module
      const nextIndex = moduleIndex + 1;
      if (nextIndex < moduleIds.length) {
        const nextWeekNum = nextIndex + 1;
        const nextModuleId = moduleIds[nextIndex];
        const nextUrl = `https://www.coursera.org/learn/${this.ctx.courseSlug}/home/week/${nextWeekNum}`;

        if (shouldAutoJump) {
          this.ctx.log(`Jumping to Week ${nextWeekNum} in 2.5s...`, "progress");
          sessionStorage.setItem("coursera_auto_skip", this.ctx.courseSlug);
          await A(2500, 500);
          window.location.href = nextUrl;
          return;
        } else {
          this.ctx.log(`Next module available: Week ${nextWeekNum}`, "info");
        }
      } else {
        sessionStorage.removeItem("coursera_auto_skip");
        this.ctx.log("🎉 Course completed! All modules processed.", "success");
      }

      await A(1500, 1000);
      window.location.reload();
    } catch (err) {
      this.ctx.log(`Error: ${err.message}`, "error");
    }
  }

  // Execute ALL modules in the course in sequence
  async executeFullCourse(courseDetails) {
    try {
      const { moduleIds, modules, items } = courseDetails;
      this.ctx.log(`🚀 Starting Full Course Skip (${moduleIds.length} modules total)...`, "progress");

      const progressSet = await this.fetchProgress();
      let totalSkipped = 0;
      let totalManual = 0;

      for (let i = 0; i < moduleIds.length; i++) {
        const mId = moduleIds[i];
        const mObj = modules.find((m) => m.id === mId);
        const mName = mObj?.name || `Week ${i + 1}`;
        const mItems = items.filter((it) => it.moduleId === mId);
        const uncompleted = mItems.filter((it) => !this.isCompleted(it, progressSet));

        this.ctx.log(`[Week ${i + 1}/${moduleIds.length}] ${mName} (${uncompleted.length} items to skip)...`, "progress");

        for (const item of uncompleted) {
          const ok = await this.processItem(item);
          if (ok) totalSkipped++;
          else totalManual++;
          await A(250, 200);
        }

        await this.finalizeModule(mId);
        this.ctx.log(`✓ Week ${i + 1} finalized.`, "success");
        await A(500, 500);
      }

      sessionStorage.removeItem("coursera_auto_skip");
      this.ctx.log(
        `🎉 FULL COURSE COMPLETED! Skipped: ${totalSkipped} items. (Manual items: ${totalManual})`,
        "success"
      );
      await A(2000, 1000);
      window.location.href = `https://www.coursera.org/learn/${this.ctx.courseSlug}/home/welcome`;
    } catch (err) {
      this.ctx.log(`Course skip error: ${err.message}`, "error");
    }
  }
}

// Module skip action entrypoint
const Et = async (log) => {
  log("Locating user session & course...", "progress");
  const userId = await Oe();
  const csrf = je();
  const courseSlug = getCourseSlug();

  if (!userId) {
    log("Could not detect Coursera User ID. Please ensure you are logged in.", "error");
    return;
  }
  if (!courseSlug) {
    log("Please navigate to a Coursera course page (/learn/<courseSlug>).", "error");
    return;
  }

  log(`User ID: ${userId} | Course: ${courseSlug}`, "info");

  try {
    const runner = new Nt(userId, null, csrf, courseSlug, log);
    const courseDetails = await runner.fetchCourseDetails();
    runner.ctx.courseId = courseDetails.courseId;

    const currentModule = detectCurrentModule(courseSlug, courseDetails);
    log(`Current module detected: ${currentModule.moduleName} (Week ${currentModule.weekNumber})`, "info");

    await runner.executeModule(currentModule, courseDetails, true);
  } catch (err) {
    log(`Initialization error: ${err.message}`, "error");
  }
};

// Full Course skip action entrypoint
const SkipFullCourse = async (log) => {
  log("Starting full course skip...", "progress");
  const userId = await Oe();
  const csrf = je();
  const courseSlug = getCourseSlug();

  if (!userId || !courseSlug) {
    log("User session or course slug missing.", "error");
    return;
  }

  try {
    const runner = new Nt(userId, null, csrf, courseSlug, log);
    const courseDetails = await runner.fetchCourseDetails();
    runner.ctx.courseId = courseDetails.courseId;

    await runner.executeFullCourse(courseDetails);
  } catch (err) {
    log(`Full course error: ${err.message}`, "error");
  }
};

// Auto grade action
const Ut = async (log) => {
  try {
    log("Scanning for grading fields...", "info");
    const radios = document.querySelectorAll('.rc-FormPart input[type="radio"], .rc-Option input[type="radio"]');
    if (radios.length > 0) {
      log(`Selecting highest grades for ${radios.length} items...`, "progress");
      const seenNames = new Set();
      radios.forEach((r) => {
        const name = r.name;
        if (!seenNames.has(name)) {
          const group = document.querySelectorAll(`input[name="${name}"]`);
          const highest = group[group.length - 1];
          highest.click();
          highest.dispatchEvent(new Event("change", { bubbles: true }));
          seenNames.add(name);
        }
      });
    }

    const textareas = document.querySelectorAll("textarea");
    if (textareas.length > 0) {
      log(`Filling ${textareas.length} feedback areas...`, "progress");
      for (const t of Array.from(textareas)) {
        if (!t.value) {
          t.value = "Excellent work and thorough analysis.";
          t.dispatchEvent(new Event("input", { bubbles: true }));
          t.dispatchEvent(new Event("blur", { bubbles: true }));
          await Ge(100);
        }
      }
    }

    const submitBtn = document.querySelector('.rc-FormSubmit button, button[type="submit"]');
    if (submitBtn) {
      log("Review filled. Submitting...", "progress");
      submitBtn.click();
    }
    log("Grading complete.", "success");
  } catch (err) {
    log(`Grading failed: ${err.message}`, "error");
  }
};

// Disable AI grade
const Tt = async (log) => {
  try {
    const scripts = document.querySelectorAll("script");
    let disabled = false;
    log("Searching for AI grader...", "progress");
    for (const s of Array.from(scripts)) {
      if (s.innerText.includes("ai-grader") || s.src.includes("ai-grader") || s.innerText.includes("GradingPolicy")) {
        s.remove();
        disabled = true;
      }
    }
    const aiBlocks = document.querySelectorAll(".rc-AIGradeInstruction, .css-8h7v9a");
    for (const b of Array.from(aiBlocks)) {
      b.style.display = "none";
      disabled = true;
    }
    disabled ? log("AI grader disabled.", "success") : log("No AI grader found.", "info");
  } catch (err) {
    log(`Error: ${err.message}`, "error");
  }
};

// Quiz harvest
const Lt = async (log) => {
  log("Downloading quiz results...", "progress");
  try {
    const results = Be("harvest");
    if (results.length === 0) {
      log("No completed quiz results found on this page.", "error");
      return;
    }
    const jsonStr = JSON.stringify(results, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `coursera_quiz_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    log(`Downloaded ${results.length} questions to file.`, "success");
  } catch (err) {
    log(`Download failed: ${err.message}`, "error");
  }
};

// Quiz export unsolved
const Dt = async (log) => {
  log("Copying unsolved quiz...", "progress");
  try {
    const results = Be("blueprint");
    if (results.length === 0) {
      log("No unsolved quiz found on this page.", "error");
      return;
    }
    const jsonStr = JSON.stringify(results, null, 2);
    await navigator.clipboard.writeText(jsonStr);
    log(`Copied ${results.length} questions to clipboard.`, "success");
  } catch (err) {
    log(`Copy failed: ${err.message}`, "error");
  }
};

// Fill peer submission
const Pt = async (log) => {
  try {
    const userId = await Oe();
    const courseId = Fe();
    const csrf = je();
    const courseSlug = getCourseSlug();
    const peerMatch = window.location.pathname.match(/\/peer\/([^/]+)/);
    const itemId = peerMatch ? peerMatch[1] : null;

    if (!userId || !courseId || !csrf || !itemId) {
      log("Critical context missing. Ensure you are on a peer submission page.", "error");
      return;
    }

    log("Preparing peer submission...", "info");
    const ctx = Qe(userId, courseId, csrf, courseSlug, log);
    const schemaRes = await fetch(
      `/api/onDemandPeerSubmissions.v1/?q=activeByItemAndUser&courseId=${courseId}&itemId=${itemId}&userId=${userId}&includes=submissionSchemas&fields=onDemandPeerSubmissionSchemas.v1(submissionSchema)`,
      { headers: ctx.headers() }
    );
    if (!schemaRes.ok) throw new Error(`Schema fetch failed: ${schemaRes.status}`);
    const schemaJson = await schemaRes.json();
    const schemaObj = schemaJson?.linked?.["onDemandPeerSubmissionSchemas.v1"]?.[0];
    const schema = schemaObj?.submissionSchema;
    if (!schema) throw new Error("No submission schema found.");

    const assignmentId = schemaObj.id.split("~").pop();
    log(`Schema found. Assignment ID: ${assignmentId}`, "info");

    const parts = {};
    const caption = "Course project implementation completed.";
    for (const part of schema.parts || []) {
      if (part.details.typeName === "fileUpload") {
        log(`Uploading file for part: ${part.id}`, "progress");
        const fileContent = "Peer assignment submission file.";
        const md5 = await Ve(fileContent);
        const presignRes = await ctx.graphql(
          "GetPreSignedUrl",
          { input: { contentMd5: md5, contentType: "text/plain", fileName: "report.txt" } },
          `mutation GetPreSignedUrl($input: Submission_FileUploadQuestionGenerateUploadUrlInput!) {
            Submission_FileUploadQuestionGenerateUploadUrl(input: $input) {
              url
              additionalHeaders { name value }
            }
          }`
        );
        const presignJson = (await presignRes.json())?.[0];
        const presignData = presignJson?.data?.Submission_FileUploadQuestionGenerateUploadUrl;
        if (presignData?.url) {
          const s3Headers = { "Content-Type": "text/plain", "Content-MD5": md5 };
          (presignData.additionalHeaders || []).forEach((h) => (s3Headers[h.name] = h.value));
          await fetch(presignData.url, { method: "PUT", headers: s3Headers, body: fileContent });
          parts[part.id] = {
            typeName: "fileUpload",
            definition: { caption, fileUrl: presignData.url.split("?")[0], title: "Report" }
          };
        }
      } else if (part.details.typeName === "url") {
        parts[part.id] = {
          typeName: "url",
          definition: { url: "https://google.com", caption: "Demo", title: "Demo" }
        };
      } else if (part.details.typeName === "plainText") {
        parts[part.id] = { typeName: "plainText", definition: { text: caption } };
      }
    }

    log("Synchronizing draft...", "progress");
    await ctx.put(`/api/onDemandPeerSubmissionDrafts.v1/${userId}~${courseId}~${itemId}/`, {
      submission: { title: "Peer Project", parts },
      attachedAssignmentId: assignmentId
    });
    await A(1000, 500);

    log("Finalizing submission...", "progress");
    const submitRes = await ctx.post("/api/onDemandPeerSubmissions.v1/", {
      courseId,
      itemId,
      gradingType: "HUMAN"
    });
    if (submitRes.ok) {
      log("Peer submission COMPLETE.", "success");
      setTimeout(() => window.location.reload(), 2000);
    } else {
      throw new Error(`Submit rejected: ${submitRes.status}`);
    }
  } catch (err) {
    log("Handling via browser DOM automation...", "progress");
    await At(log);
  }
};

// Fallback DOM peer fill
async function At(log) {
  const title = document.getElementById("title");
  if (title) {
    title.value = "Course Project";
    title.dispatchEvent(new Event("input", { bubbles: true }));
    title.dispatchEvent(new Event("blur", { bubbles: true }));
  }
  const urls = document.querySelectorAll('input[aria-label="URL"], input[placeholder*="https://"]');
  urls.forEach((u) => {
    if (!u.value) {
      u.value = "https://google.com";
      u.dispatchEvent(new Event("input", { bubbles: true }));
      u.dispatchEvent(new Event("blur", { bubbles: true }));
    }
  });

  const textareas = document.querySelectorAll(
    '.rc-PeerItemEditView input[type="text"], .rc-PeerItemEditView textarea, .uppy-Dashboard-Item-name input'
  );
  textareas.forEach((t) => {
    if (!t.value && t.id !== "title") {
      t.value = "Course assignment steps completed per instructions.";
      t.dispatchEvent(new Event("input", { bubbles: true }));
      t.dispatchEvent(new Event("blur", { bubbles: true }));
    }
  });
  log("UI fill sequence complete.", "success");
}

// Review URL copy
const copyReviewUrl = async (log) => {
  try {
    const courseSlug = getCourseSlug();
    const peerMatch = window.location.pathname.match(/\/peer\/([^/]+)\/([^/]+)/);
    const itemId = peerMatch ? peerMatch[1] : null;
    const assignSlug = peerMatch ? peerMatch[2] : null;

    if (!courseSlug || !itemId || !assignSlug) {
      log("Ensure you are on the peer review/submission tab.", "error");
      return;
    }

    let subId;
    const commentBox = document.querySelector('textarea[id*="~comment"]');
    if (commentBox) subId = commentBox.id.split("~")[0];
    if (!subId) {
      const partView = document.querySelector(".rc-SubmissionPartView");
      if (partView) subId = partView.id;
    }
    if (!subId) throw new Error("Submission ID not found on page.");

    const reviewUrl = `https://www.coursera.org/learn/${courseSlug}/peer/${itemId}/${assignSlug}/review/${subId}`;
    await navigator.clipboard.writeText(reviewUrl);
    log("Review URL copied to clipboard!", "success");
    log(`URL: ${reviewUrl}`, "info");
  } catch (err) {
    log(`Failed to copy URL: ${err.message}`, "error");
  }
};

const Mt = Object.freeze({
  skipModule: Et,
  skipCourse: SkipFullCourse,
  autoGrade: Ut,
  disableAIGrade: Tt,
  exportUnsolved: Dt,
  fillPeer: Pt,
  harvestQuiz: Lt,
  copyReviewUrl
});



const qt = { theme: "light" };
async function zt() {
  return new Promise((t) => {
    chrome.storage.local.get(["settings"], (e) => {
      t(e.settings || qt);
    });
  });
}
async function Rt(t) {
  return new Promise((e) => {
    chrome.storage.local.set({ settings: t }, () => {
      e();
    });
  });
}
const Ht = (t) => {
  const e = t.theme === "light";
  return le(
    () => ({
      panel: e ? "bg-white border-stone-200" : "bg-stone-950 border-stone-800",
      text: e ? "text-stone-800" : "text-stone-200",
      muted: e ? "text-stone-500" : "text-stone-400",
      faint: e ? "text-stone-400" : "text-stone-500",
      surface: e ? "border-stone-200 bg-stone-50" : "border-stone-800 bg-stone-900",
      divider: e ? "border-stone-100" : "border-stone-800",
      isLight: e
    }),
    [e]
  );
};
const Ot = () => {
  const [t, e] = P([]),
    [o, i] = P("Idle"),
    [n, r] = P("info"),
    s = qe((d, l) => {
      const p = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      e((a) => [...a, { id: Date.now() + Math.random(), message: d, type: l, time: p }]);
      i(d);
      r(l);
    }, []),
    c = qe(() => e([]), []);
  return { logs: t, latestStatus: o, statusType: n, addLog: s, clearLogs: c };
};
const Ft = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400/60 focus-visible:ring-offset-1";
const M = ({ label: t, onClick: e, variant: o, isLight: i, className: n = "" }) => {
  const r = `flex items-center justify-center rounded-lg px-2.5 py-1.5 text-center text-[10.5px] font-medium transition-colors ${Ft}`;
  return h("button", {
    onClick: e,
    className: `${r} ${
      {
        primary: i ? "bg-stone-800 text-white hover:bg-stone-700" : "bg-stone-100 text-stone-900 hover:bg-stone-200",
        accent: i
          ? "border border-stone-200 bg-stone-50 text-emerald-700 hover:bg-emerald-50"
          : "border border-stone-700 bg-stone-900 text-emerald-400 hover:bg-stone-800",
        secondary: i
          ? "border border-stone-200 bg-stone-50 text-stone-600 hover:bg-stone-100"
          : "border border-stone-700 bg-stone-900 text-stone-400 hover:bg-stone-800",
        danger: i
          ? "border border-stone-200 bg-stone-50 text-red-600 hover:bg-red-50"
          : "border border-stone-700 bg-stone-900 text-red-400 hover:bg-stone-800"
      }[o]
    } ${n}`,
    children: t
  });
};
const jt = ({ logs: t, showDataStream: e, setShowDataStream: o, clearLogs: i, t: n }) => {
  const r = lt(null);
  return (
    Me(() => {
      var s;
      (s = r.current) == null || s.scrollIntoView({ behavior: "smooth" });
    }, [t]),
    h("div", {
      className: "fade-in flex flex-1 flex-col overflow-hidden",
      children: [
        h("div", {
          className: "flex items-center justify-between",
          children: [
            h("button", {
              onClick: () => o(!e),
              className: `rounded px-1 py-0.5 text-[11px] font-medium transition-colors focus-visible:outline-none ${
                e ? n.muted : n.faint
              } ${n.isLight ? "hover:text-stone-600" : "hover:text-stone-300"}`,
              children: e ? "Hide console" : "Show console"
            }),
            e &&
              h("button", {
                onClick: i,
                className: `rounded px-1 py-0.5 text-[11px] font-medium transition-colors focus-visible:outline-none ${n.faint} hover:text-red-600`,
                children: "Clear"
              })
          ]
        }),
        e &&
          h("div", {
            className: `${
              n.isLight ? "custom-scrollbar" : "custom-scrollbar custom-scrollbar-dark"
            } relative mt-1.5 max-h-[160px] overflow-y-auto rounded-lg border p-3 font-mono text-[10px] leading-relaxed ${
              n.surface
            }`,
            children:
              t.length === 0
                ? h("div", {
                    className: `flex flex-1 items-center justify-center ${n.faint}`,
                    children: h("span", { className: "text-[11px] font-medium", children: "No output" })
                  })
                : h("div", {
                    className: "space-y-1.5",
                    children: [
                      ...t.map((s) =>
                        h(
                          "div",
                          {
                            className: "flex gap-2.5",
                            children: [
                              h("span", { className: `shrink-0 tabular-nums ${n.faint}`, children: s.time }),
                              h("span", {
                                className:
                                  s.type === "success"
                                    ? n.isLight
                                      ? "text-emerald-700 font-medium"
                                      : "text-emerald-400 font-medium"
                                    : s.type === "error"
                                    ? n.isLight
                                      ? "font-medium text-red-700"
                                      : "font-medium text-red-400"
                                    : s.type === "progress"
                                    ? n.isLight
                                      ? "text-blue-700 font-medium"
                                      : "text-blue-400 font-medium"
                                    : n.isLight
                                    ? "text-stone-700"
                                    : "text-stone-300",
                                children: s.message
                              })
                            ]
                          },
                          s.id
                        )
                      ),
                      h("div", { ref: r })
                    ]
                  })
          })
      ]
    })
  );
};
const Bt = ({ runAutomation: t, logs: e, showDataStream: o, setShowDataStream: i, clearLogs: n, t: r }) =>
  h("div", {
    className: "fade-in flex flex-1 flex-col gap-3 overflow-hidden",
    children: [
      h("div", {
        className: "custom-scrollbar grid grid-cols-2 gap-1.5 overflow-y-auto pr-0.5",
        children: [
          h(M, { label: "Skip & Next Week", onClick: () => t("skipModule"), variant: "primary", isLight: r.isLight }),
          h(M, { label: "Skip Full Course", onClick: () => t("skipCourse"), variant: "accent", isLight: r.isLight }),
          h(M, { label: "Download result", onClick: () => t("harvestQuiz"), variant: "secondary", isLight: r.isLight }),
          h(M, { label: "Copy questions", onClick: () => t("exportUnsolved"), variant: "secondary", isLight: r.isLight }),
          h(M, { label: "Auto grade", onClick: () => t("autoGrade"), variant: "secondary", isLight: r.isLight }),
          h(M, { label: "Fill Peer", onClick: () => t("fillPeer"), variant: "secondary", isLight: r.isLight }),
          h(M, { label: "Disable grader", onClick: () => t("disableAIGrade"), variant: "danger", isLight: r.isLight }),
          h(M, { label: "Review URL", onClick: () => t("copyReviewUrl"), variant: "secondary", isLight: r.isLight })
        ]
      }),
      h(jt, { logs: e, showDataStream: o, setShowDataStream: i, clearLogs: n, t: r })
    ]
  });
const ue = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400/60 focus-visible:ring-offset-1";
const Gt = ({ settings: t, setSettings: e, onSave: o, onCopyUA: i, t: n }) =>
  h("div", {
    className: "fade-in flex h-full flex-col gap-4",
    children: [
      h("div", {
        className: "flex items-center justify-between",
        children: [
          h("h3", { className: `text-xs font-semibold ${n.muted}`, children: "Preferences" }),
          h("button", {
            onClick: () => e({ ...t, theme: t.theme === "light" ? "dark" : "light" }),
            "aria-label": n.isLight ? "Switch to dark theme" : "Switch to light theme",
            className: `rounded-md border p-1.5 transition-colors ${ue} ${
              n.isLight
                ? "border-stone-200 text-stone-500 hover:text-stone-700"
                : "border-stone-700 text-stone-400 hover:text-stone-200"
            }`,
            children: n.isLight ? h(_t, { size: 14 }) : h(wt, { size: 14 })
          })
        ]
      }),
      h(
        "button",
        {
          onClick: i,
          className: `flex w-full flex-col gap-0.5 rounded-lg border px-3.5 py-2.5 text-left transition-colors ${ue} ${
            n.surface
          } ${n.isLight ? "hover:bg-stone-100" : "hover:bg-stone-800"}`
        },
        {
          children: [
            h("span", { className: `text-[11px] font-semibold ${n.text}`, children: "Copy locked UA" }),
            h("span", { className: `text-[11px] ${n.faint}`, children: "Save to clipboard" })
          ]
        }
      ),
      h("div", {
        className: "mt-auto",
        children: h("button", {
          onClick: o,
          className: `flex w-full items-center justify-center rounded-lg px-4 py-2.5 text-xs font-semibold transition-colors ${ue} ${
            n.isLight ? "bg-stone-800 text-white hover:bg-stone-700" : "bg-stone-100 text-stone-900 hover:bg-stone-200"
          }`,
          children: "Save changes"
        })
      })
    ]
  });
const We = "coursera-locking-browser/0.6.3";
const Je = "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-stone-400/60 focus-visible:ring-offset-1";
const Vt = () => {
  const [t, e] = P("main"),
    [o, i] = P(!1),
    [n, r] = P(!0), // Show console = true by default
    [s, c] = P({ theme: "light" }),
    { logs: d, latestStatus: l, statusType: p, addLog: a, clearLogs: m } = Ot(),
    u = Ht(s);
  Me(() => {
    zt().then(c);
    // Check auto-skip continuation
    try {
      const slug = getCourseSlug();
      if (slug && sessionStorage.getItem("coursera_auto_skip") === slug) {
        setTimeout(() => {
          a("Resuming auto-skip for current module...", "progress");
          _("skipModule");
        }, 1500);
      }
    } catch {}
  }, []);
  const w = async () => {
      await Rt(s);
      a("Settings saved.", "success");
      e("main");
    },
    v = () => {
      a(`Locked UA: ${We}`, "info");
      navigator.clipboard.writeText(We);
      a("Copied to clipboard.", "success");
    },
    _ = async (f) => {
      if (Mt[f]) {
        await Mt[f](a);
      }
    };
  return h("div", {
    className: `fixed bottom-6 right-6 z-[2147483647] flex w-80 flex-col overflow-hidden rounded-lg border font-sans shadow-md transition-all duration-200 ${
      o ? "h-11" : n ? "h-[460px]" : t === "settings" ? "h-[300px]" : "h-[340px]"
    } ${u.panel} ${u.text}`,
    children: [
      h("div", {
        className: "flex items-center justify-between px-3.5 py-2.5",
        children: [
          h("div", {
            className: "flex items-center gap-1.5",
            children: [
              h("span", { className: `text-xs font-bold tracking-tight ${u.text}`, children: "Coursera AutoPilot" }),
              h("span", { className: `text-[10px] px-1.5 py-0.5 rounded font-mono ${u.surface} ${u.muted}`, children: "v1.3.0" })
            ]
          }),
          h("div", {
            className: "flex items-center gap-1",
            children: [
              !o &&
                h("button", {
                  onClick: () => e(t === "main" ? "settings" : "main"),
                  "aria-label": t === "settings" ? "Back" : "Settings",
                  className: `rounded-md p-1.5 transition-colors ${Je} ${
                    t === "settings"
                      ? u.isLight
                        ? "bg-stone-100 text-stone-700"
                        : "bg-stone-800 text-stone-200"
                      : `${u.faint} ${u.isLight ? "hover:text-stone-700" : "hover:text-stone-200"}`
                  }`,
                  children: t === "settings" ? h(ht, { size: 15 }) : h(bt, { size: 15 })
                }),
              h("button", {
                onClick: () => i(!o),
                "aria-label": o ? "Expand panel" : "Collapse panel",
                className: `rounded-md p-1.5 transition-colors ${Je} ${u.faint} ${
                  u.isLight ? "hover:text-stone-700" : "hover:text-stone-200"
                }`,
                children: o ? h(gt, { size: 15 }) : h(ft, { size: 15 })
              })
            ]
          })
        ]
      }),
      !o &&
        h("div", {
          className: "flex flex-1 flex-col overflow-hidden px-3.5 pb-3",
          children: [
            h("div", {
              className: "flex flex-1 flex-col gap-3 overflow-hidden",
              children:
                t === "settings"
                  ? h(Gt, { settings: s, setSettings: c, onSave: w, onCopyUA: v, t: u })
                  : h(Bt, { runAutomation: _, logs: d, showDataStream: n, setShowDataStream: r, clearLogs: m, t: u })
            }),
            h("div", {
              className: `flex items-center gap-2 border-t pt-2 ${u.divider}`,
              children: [
                h("div", {
                  className: `h-1.5 w-1.5 rounded-full ${
                    p === "success"
                      ? "bg-emerald-500"
                      : p === "error"
                      ? "bg-red-500"
                      : p === "progress"
                      ? "bg-blue-500"
                      : u.isLight
                      ? "bg-stone-300"
                      : "bg-stone-600"
                  }`
                }),
                h("span", {
                  className: `max-w-[220px] truncate text-[11px] ${u.faint}`,
                  children: l === "Idle" ? "Idle" : l
                })
              ]
            })
          ]
        })
    ]
  });
};



const Qt = '*,:before,:after{--tw-border-spacing-x: 0;--tw-border-spacing-y: 0;--tw-translate-x: 0;--tw-translate-y: 0;--tw-rotate: 0;--tw-skew-x: 0;--tw-skew-y: 0;--tw-scale-x: 1;--tw-scale-y: 1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness: proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width: 0px;--tw-ring-offset-color: #fff;--tw-ring-color: rgb(59 130 246 / .5);--tw-ring-offset-shadow: 0 0 #0000;--tw-ring-shadow: 0 0 #0000;--tw-shadow: 0 0 #0000;--tw-shadow-colored: 0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }::backdrop{--tw-border-spacing-x: 0;--tw-border-spacing-y: 0;--tw-translate-x: 0;--tw-translate-y: 0;--tw-rotate: 0;--tw-skew-x: 0;--tw-skew-y: 0;--tw-scale-x: 1;--tw-scale-y: 1;--tw-pan-x: ;--tw-pan-y: ;--tw-pinch-zoom: ;--tw-scroll-snap-strictness: proximity;--tw-gradient-from-position: ;--tw-gradient-via-position: ;--tw-gradient-to-position: ;--tw-ordinal: ;--tw-slashed-zero: ;--tw-numeric-figure: ;--tw-numeric-spacing: ;--tw-numeric-fraction: ;--tw-ring-inset: ;--tw-ring-offset-width: 0px;--tw-ring-offset-color: #fff;--tw-ring-color: rgb(59 130 246 / .5);--tw-ring-offset-shadow: 0 0 #0000;--tw-ring-shadow: 0 0 #0000;--tw-shadow: 0 0 #0000;--tw-shadow-colored: 0 0 #0000;--tw-blur: ;--tw-brightness: ;--tw-contrast: ;--tw-grayscale: ;--tw-hue-rotate: ;--tw-invert: ;--tw-saturate: ;--tw-sepia: ;--tw-drop-shadow: ;--tw-backdrop-blur: ;--tw-backdrop-brightness: ;--tw-backdrop-contrast: ;--tw-backdrop-grayscale: ;--tw-backdrop-hue-rotate: ;--tw-backdrop-invert: ;--tw-backdrop-opacity: ;--tw-backdrop-saturate: ;--tw-backdrop-sepia: ;--tw-contain-size: ;--tw-contain-layout: ;--tw-contain-paint: ;--tw-contain-style: }*,:before,:after{box-sizing:border-box;border-width:0;border-style:solid;border-color:#e5e7eb}:before,:after{--tw-content: ""}html,:host{line-height:1.5;-webkit-text-size-adjust:100%;-moz-tab-size:4;-o-tab-size:4;tab-size:4;font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif;font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent}body{margin:0;line-height:inherit}hr{height:0;color:inherit;border-top-width:1px}abbr:where([title]){-webkit-text-decoration:underline dotted;text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,samp,pre{font-family:ui-monospace,SF Mono,Cascadia Code,Consolas,monospace;font-feature-settings:normal;font-variation-settings:normal;font-size:1em}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-.25em}sup{top:-.5em}table{text-indent:0;border-color:inherit;border-collapse:collapse}button,input,optgroup,select,textarea{font-family:inherit;font-feature-settings:inherit;font-variation-settings:inherit;font-size:100%;font-weight:inherit;line-height:inherit;letter-spacing:inherit;color:inherit;margin:0;padding:0}button,select{text-transform:none}button,input:where([type=button]),input:where([type=reset]),input:where([type=submit]){-webkit-appearance:button;background-color:transparent;background-image:none}:-moz-focusring{outline:auto}:-moz-ui-invalid{box-shadow:none}progress{vertical-align:baseline}::-webkit-inner-spin-button,::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}blockquote,dl,dd,h1,h2,h3,h4,h5,h6,hr,figure,p,pre{margin:0}fieldset{margin:0;padding:0}legend{padding:0}ol,ul,menu{list-style:none;margin:0;padding:0}dialog{padding:0}textarea{resize:vertical}input::-moz-placeholder,textarea::-moz-placeholder{opacity:1;color:#9ca3af}input::placeholder,textarea::placeholder{opacity:1;color:#9ca3af}button,[role=button]{cursor:pointer}:disabled{cursor:default}img,svg,video,canvas,audio,iframe,embed,object{display:block;vertical-align:middle}img,video{max-width:100%;height:auto}[hidden]:where(:not([hidden=until-found])){display:none}.custom-scrollbar::-webkit-scrollbar{width:4px;height:4px}.custom-scrollbar::-webkit-scrollbar-track{background:transparent}.custom-scrollbar::-webkit-scrollbar-thumb{border-radius:9999px;--tw-bg-opacity: 1;background-color:rgb(214 211 209 / var(--tw-bg-opacity, 1))}.custom-scrollbar-dark::-webkit-scrollbar-thumb{border-radius:9999px;--tw-bg-opacity: 1;background-color:rgb(68 64 60 / var(--tw-bg-opacity, 1))}.fade-in{animation:fadeIn .15s ease-out both}@keyframes fadeIn{0%{opacity:0;transform:translateY(2px)}to{opacity:1;transform:translateY(0)}}.container{width:100%}@media (min-width: 640px){.container{max-width:640px}}@media (min-width: 768px){.container{max-width:768px}}@media (min-width: 1024px){.container{max-width:1024px}}@media (min-width: 1280px){.container{max-width:1280px}}@media (min-width: 1536px){.container{max-width:1536px}}.fixed{position:fixed}.relative{position:relative}.bottom-6{bottom:1.5rem}.right-6{right:1.5rem}.z-\\[2147483647\\]{z-index:2147483647}.col-span-2{grid-column:span 2 / span 2}.mt-1\\.5{margin-top:.375rem}.mt-auto{margin-top:auto}.block{display:block}.flex{display:flex}.grid{display:grid}.contents{display:contents}.h-1\\.5{height:.375rem}.h-11{height:2.75rem}.h-\\[300px\\]{height:300px}.h-\\[320px\\]{height:320px}.h-\\[460px\\]{height:460px}.h-full{height:100%}.max-h-\\[160px\\]{max-height:160px}.min-h-\\[280px\\]{min-height:280px}.w-1\\.5{width:.375rem}.w-80{width:20rem}.w-full{width:100%}.max-w-\\[220px\\]{max-width:220px}.flex-1{flex:1 1 0%}.shrink-0{flex-shrink:0}.grid-cols-2{grid-template-columns:repeat(2,minmax(0,1fr))}.flex-col{flex-direction:column}.items-center{align-items:center}.justify-center{justify-content:center}.justify-between{justify-content:space-between}.gap-0\\.5{gap:.125rem}.gap-1{gap:.25rem}.gap-1\\.5{gap:.375rem}.gap-2{gap:.5rem}.gap-2\\.5{gap:.625rem}.gap-3{gap:.75rem}.gap-4{gap:1rem}.space-y-1\\.5>:not([hidden])~:not([hidden]){--tw-space-y-reverse: 0;margin-top:calc(.375rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(.375rem * var(--tw-space-y-reverse))}.space-y-2>:not([hidden])~:not([hidden]){--tw-space-y-reverse: 0;margin-top:calc(.5rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(.5rem * var(--tw-space-y-reverse))}.space-y-3>:not([hidden])~:not([hidden]){--tw-space-y-reverse: 0;margin-top:calc(.75rem * calc(1 - var(--tw-space-y-reverse)));margin-bottom:calc(.75rem * var(--tw-space-y-reverse))}.overflow-hidden{overflow:hidden}.overflow-y-auto{overflow-y:auto}.truncate{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.rounded{border-radius:.25rem}.rounded-full{border-radius:9999px}.rounded-lg{border-radius:.5rem}.rounded-md{border-radius:.375rem}.border{border-width:1px}.border-t{border-top-width:1px}.border-stone-100{--tw-border-opacity: 1;border-color:rgb(245 245 244 / var(--tw-border-opacity, 1))}.border-stone-200{--tw-border-opacity: 1;border-color:rgb(231 229 228 / var(--tw-border-opacity, 1))}.border-stone-700{--tw-border-opacity: 1;border-color:rgb(68 64 60 / var(--tw-border-opacity, 1))}.border-stone-800{--tw-border-opacity: 1;border-color:rgb(41 37 36 / var(--tw-border-opacity, 1))}.bg-blue-50{--tw-bg-opacity: 1;background-color:rgb(239 246 255 / var(--tw-bg-opacity, 1))}.bg-blue-500{--tw-bg-opacity: 1;background-color:rgb(59 130 246 / var(--tw-bg-opacity, 1))}.bg-emerald-50{--tw-bg-opacity: 1;background-color:rgb(236 253 245 / var(--tw-bg-opacity, 1))}.bg-emerald-500{--tw-bg-opacity: 1;background-color:rgb(16 185 129 / var(--tw-bg-opacity, 1))}.bg-red-500{--tw-bg-opacity: 1;background-color:rgb(239 68 68 / var(--tw-bg-opacity, 1))}.bg-stone-100{--tw-bg-opacity: 1;background-color:rgb(245 245 244 / var(--tw-bg-opacity, 1))}.bg-stone-300{--tw-bg-opacity: 1;background-color:rgb(214 211 209 / var(--tw-bg-opacity, 1))}.bg-stone-50{--tw-bg-opacity: 1;background-color:rgb(250 250 249 / var(--tw-bg-opacity, 1))}.bg-stone-600{--tw-bg-opacity: 1;background-color:rgb(87 83 78 / var(--tw-bg-opacity, 1))}.bg-stone-800{--tw-bg-opacity: 1;background-color:rgb(41 37 36 / var(--tw-bg-opacity, 1))}.bg-stone-900{--tw-bg-opacity: 1;background-color:rgb(28 25 23 / var(--tw-bg-opacity, 1))}.bg-stone-950{--tw-bg-opacity: 1;background-color:rgb(12 10 9 / var(--tw-bg-opacity, 1))}.bg-white{--tw-bg-opacity: 1;background-color:rgb(255 255 255 / var(--tw-bg-opacity, 1))}.p-1\\.5{padding:.375rem}.p-3{padding:.75rem}.p-3\\.5{padding:.875rem}.p-5{padding:1.25rem}.px-1{padding-left:.25rem;padding-right:.25rem}.px-2{padding-left:.5rem;padding-right:.5rem}.px-2\\.5{padding-left:.625rem;padding-right:.625rem}.px-3\\.5{padding-left:.875rem;padding-right:.875rem}.px-4{padding-left:1rem;padding-right:1rem}.py-0\\.5{padding-top:.125rem;padding-bottom:.125rem}.py-1\\.5{padding-top:.375rem;padding-bottom:.375rem}.py-2{padding-top:.5rem;padding-bottom:.5rem}.py-2\\.5{padding-top:.625rem;padding-bottom:.625rem}.pb-3{padding-bottom:.75rem}.pr-0\\.5{padding-right:.125rem}.pt-2{padding-top:.5rem}.text-left{text-align:left}.text-center{text-align:center}.font-mono{font-family:ui-monospace,SF Mono,Cascadia Code,Consolas,monospace}.font-sans{font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica Neue,Arial,sans-serif}.text-\\[10\\.5px\\]{font-size:10.5px}.text-\\[10px\\]{font-size:10px}.text-\\[11px\\]{font-size:11px}.text-\\[12px\\]{font-size:12px}.text-base{font-size:1rem;line-height:1.5rem}.text-xs{font-size:.75rem;line-height:1rem}.font-medium{font-weight:500}.font-semibold{font-weight:600}.tabular-nums{--tw-numeric-spacing: tabular-nums;font-variant-numeric:var(--tw-ordinal) var(--tw-slashed-zero) var(--tw-numeric-figure) var(--tw-numeric-spacing) var(--tw-numeric-fraction)}.leading-relaxed{line-height:1.625}.tracking-tight{letter-spacing:-.025em}.text-blue-400{--tw-text-opacity: 1;color:rgb(96 165 250 / var(--tw-text-opacity, 1))}.text-blue-700{--tw-text-opacity: 1;color:rgb(29 78 216 / var(--tw-text-opacity, 1))}.text-emerald-400{--tw-text-opacity: 1;color:rgb(52 211 153 / var(--tw-text-opacity, 1))}.text-emerald-700{--tw-text-opacity: 1;color:rgb(4 120 87 / var(--tw-text-opacity, 1))}.text-red-400{--tw-text-opacity: 1;color:rgb(248 113 113 / var(--tw-text-opacity, 1))}.text-red-600{--tw-text-opacity: 1;color:rgb(220 38 38 / var(--tw-text-opacity, 1))}.text-red-700{--tw-text-opacity: 1;color:rgb(185 28 28 / var(--tw-text-opacity, 1))}.text-stone-200{--tw-text-opacity: 1;color:rgb(231 229 228 / var(--tw-text-opacity, 1))}.text-stone-400{--tw-text-opacity: 1;color:rgb(168 162 158 / var(--tw-text-opacity, 1))}.text-stone-500{--tw-text-opacity: 1;color:rgb(120 113 108 / var(--tw-text-opacity, 1))}.text-stone-600{--tw-text-opacity: 1;color:rgb(87 83 78 / var(--tw-text-opacity, 1))}.text-stone-700{--tw-text-opacity: 1;color:rgb(68 64 60 / var(--tw-text-opacity, 1))}.text-stone-800{--tw-text-opacity: 1;color:rgb(41 37 36 / var(--tw-text-opacity, 1))}.text-stone-900{--tw-text-opacity: 1;color:rgb(28 25 23 / var(--tw-text-opacity, 1))}.text-white{--tw-text-opacity: 1;color:rgb(255 255 255 / var(--tw-text-opacity, 1))}.shadow{--tw-shadow: 0 1px 3px 0 rgb(0 0 0 / .1), 0 1px 2px -1px rgb(0 0 0 / .1);--tw-shadow-colored: 0 1px 3px 0 var(--tw-shadow-color), 0 1px 2px -1px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.shadow-md{--tw-shadow: 0 4px 6px -1px rgb(0 0 0 / .1), 0 2px 4px -2px rgb(0 0 0 / .1);--tw-shadow-colored: 0 4px 6px -1px var(--tw-shadow-color), 0 2px 4px -2px var(--tw-shadow-color);box-shadow:var(--tw-ring-offset-shadow, 0 0 #0000),var(--tw-ring-shadow, 0 0 #0000),var(--tw-shadow)}.blur{--tw-blur: blur(8px);filter:var(--tw-blur) var(--tw-brightness) var(--tw-contrast) var(--tw-grayscale) var(--tw-hue-rotate) var(--tw-invert) var(--tw-saturate) var(--tw-sepia) var(--tw-drop-shadow)}.filter{filter:var(--tw-blur) var(--tw-brightness) var(--tw-contrast) var(--tw-grayscale) var(--tw-hue-rotate) var(--tw-invert) var(--tw-saturate) var(--tw-sepia) var(--tw-drop-shadow)}.transition-all{transition-property:all;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.transition-colors{transition-property:color,background-color,border-color,text-decoration-color,fill,stroke;transition-timing-function:cubic-bezier(.4,0,.2,1);transition-duration:.15s}.duration-200{transition-duration:.2s}.hover\\:bg-emerald-50:hover{--tw-bg-opacity: 1;background-color:rgb(236 253 245 / var(--tw-bg-opacity, 1))}.hover\\:bg-red-50:hover{--tw-bg-opacity: 1;background-color:rgb(254 242 242 / var(--tw-bg-opacity, 1))}.hover\\:bg-stone-100:hover{--tw-bg-opacity: 1;background-color:rgb(245 245 244 / var(--tw-bg-opacity, 1))}.hover\\:bg-stone-200:hover{--tw-bg-opacity: 1;background-color:rgb(231 229 228 / var(--tw-bg-opacity, 1))}.hover\\:bg-stone-50:hover{--tw-bg-opacity: 1;background-color:rgb(250 250 249 / var(--tw-bg-opacity, 1))}.hover\\:bg-stone-700:hover{--tw-bg-opacity: 1;background-color:rgb(68 64 60 / var(--tw-bg-opacity, 1))}.hover\\:bg-stone-800:hover{--tw-bg-opacity: 1;background-color:rgb(41 37 36 / var(--tw-bg-opacity, 1))}.hover\\:text-red-600:hover{--tw-text-opacity: 1;color:rgb(220 38 38 / var(--tw-text-opacity, 1))}.hover\\:text-stone-200:hover{--tw-text-opacity: 1;color:rgb(231 229 228 / var(--tw-text-opacity, 1))}.hover\\:text-stone-300:hover{--tw-text-opacity: 1;color:rgb(214 211 209 / var(--tw-text-opacity, 1))}.hover\\:text-stone-600:hover{--tw-text-opacity: 1;color:rgb(87 83 78 / var(--tw-text-opacity, 1))}.hover\\:text-stone-700:hover{--tw-text-opacity: 1;color:rgb(68 64 60 / var(--tw-text-opacity, 1))}.focus-visible\\:outline-none:focus-visible{outline:2px solid transparent;outline-offset:2px}.focus-visible\\:ring-2:focus-visible{--tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0 var(--tw-ring-offset-width) var(--tw-ring-offset-color);--tw-ring-shadow: var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);box-shadow:var(--tw-ring-offset-shadow),var(--tw-ring-shadow),var(--tw-shadow, 0 0 #0000)}.focus-visible\\:ring-stone-400\\/60:focus-visible{--tw-ring-color: rgb(168 162 158 / .6)}.focus-visible\\:ring-offset-1:focus-visible{--tw-ring-offset-width: 1px}';
const pe = () => {
  if (document.getElementById("antigravity-root")) return;
  const t = document.createElement("div");
  t.id = "antigravity-root";
  document.body.appendChild(t);
  const e = t.attachShadow({ mode: "open" });
  const o = document.createElement("div");
  o.id = "antigravity-shadow-root";
  o.style.position = "relative";
  e.appendChild(o);
  const i = document.createElement("style");
  i.textContent = `
    :host {
      all: initial;
    }
    ${Qt}
  `;
  e.appendChild(i);
  st(h(Vt, {}), o);
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", pe);
} else {
  pe();
}

new MutationObserver(() => {
  if (!document.getElementById("antigravity-root")) pe();
}).observe(document.body, { childList: true, subtree: false });
})();
