(self.webpackChunk_streamlit_app=self.webpackChunk_streamlit_app||[]).push([[5618],{68035:(e,t,r)=>{"use strict";r.d(t,{A:()=>u});r(58878);var n=r(25571),o=r(78286),i=r(89653);const a=r(60667).i7`
  50% {
    color: rgba(0, 0, 0, 0);
  }
`,l=(0,i.A)("span",{target:"edlqvik0"})((e=>{let{includeDot:t,shouldBlink:r,theme:n}=e;return{...t?{"&::before":{opacity:1,content:'"\u2022"',animation:"none",color:n.colors.gray,margin:`0 ${n.spacing.twoXS}`}}:{},...r?{color:n.colors.red,animationName:`${a}`,animationDuration:"0.5s",animationIterationCount:5}:{}}}),"");var s=r(90782);const u=e=>{let{dirty:t,value:r,inForm:i,maxLength:a,className:u,type:c="single",allowEnterToSubmit:d=!0}=e;const f=[],p=function(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];f.push((0,s.jsx)(l,{includeDot:f.length>0,shouldBlink:t,children:e},f.length))};if(d){const e=i?"submit form":"apply";if("multiline"===c){p(`Press ${(0,n.u_)()?"\u2318":"Ctrl"}+Enter to ${e}`)}else"single"===c&&p(`Press Enter to ${e}`)}return a&&("chat"!==c||t)&&p(`${r.length}/${a}`,t&&r.length>=a),(0,s.jsx)(o.tp,{"data-testid":"InputInstructions",className:u,children:f})}},34752:(e,t,r)=>{"use strict";r.d(t,{X:()=>a,o:()=>i});var n=r(58878),o=r(25571);class i{constructor(){this.formClearListener=void 0,this.lastWidgetMgr=void 0,this.lastFormId=void 0}manageFormClearListener(e,t,r){(0,o.se)(this.formClearListener)&&this.lastWidgetMgr===e&&this.lastFormId===t||(this.disconnect(),(0,o._L)(t)&&(this.formClearListener=e.addFormClearedListener(t,r),this.lastWidgetMgr=e,this.lastFormId=t))}disconnect(){var e;null===(e=this.formClearListener)||void 0===e||e.disconnect(),this.formClearListener=void 0,this.lastWidgetMgr=void 0,this.lastFormId=void 0}}function a(e){let{element:t,widgetMgr:r,onFormCleared:i}=e;(0,n.useEffect)((()=>{if(!(0,o._L)(t.formId))return;const e=r.addFormClearedListener(t.formId,i);return()=>{e.disconnect()}}),[t,r,i])}},25618:(e,t,r)=>{"use strict";r.r(t),r.d(t,{default:()=>w});var n=r(58878),o=r(94928),i=r(8151),a=r(32698),l=r.n(a),s=r(68035),u=r(70474),c=r(78286),d=r(93480),f=r(997),p=r(25571),m=r(3101),g=r(90782);const h=(e,t)=>{var r,n;return null!==(r=null!==(n=e.getStringValue(t))&&void 0!==n?n:t.default)&&void 0!==r?r:null},y=e=>{var t;return null!==(t=e.default)&&void 0!==t?t:null},b=e=>{var t;return null!==(t=e.value)&&void 0!==t?t:null},v=(e,t,r,n)=>{t.setStringValue(e,r.value,{fromUi:r.fromUi},n)},S=e=>{var t,r;let{disabled:a,element:S,widgetMgr:w,fragmentId:O,width:C}=e;const F=(0,n.useRef)(l()("text_area_")).current,[j,x]=(0,n.useState)(!1),[I,P]=(0,n.useState)(!1),[E,T]=(0,n.useState)(null!==(t=h(w,S))&&void 0!==t?t:null),W=(0,n.useCallback)((()=>{var e;T(null!==(e=S.default)&&void 0!==e?e:null),x(!0)}),[S]),[M,k]=(0,m.t)({getStateFromWidgetMgr:h,getDefaultStateFromProto:y,getCurrStateFromProto:b,updateWidgetMgrState:v,element:S,widgetMgr:w,fragmentId:O,onFormCleared:W});(0,n.useEffect)((()=>{j||M!==E&&T(M)}),[M,E,j]);const $=(0,i.u)(),_=(0,n.useCallback)((e=>{let{fromUi:t}=e;k({value:E,fromUi:t}),x(!1)}),[E,k]),A=(0,n.useCallback)((()=>{j&&_({fromUi:!0}),P(!1)}),[j,_]),D=(0,n.useCallback)((()=>{P(!0)}),[]),R=(0,n.useCallback)((e=>{const{value:t}=e.target,{maxChars:r}=S;0!==r&&t.length>r||(T(t),x(!0))}),[S]),L=(0,n.useCallback)((e=>{const{metaKey:t,ctrlKey:r}=e,{formId:n}=S,o=w.allowFormEnterToSubmit(n);(e=>{var t;const{keyCode:r,key:n}=e;return("Enter"===n||13===r||10===r)&&!(!0===(null===(t=e.nativeEvent)||void 0===t?void 0:t.isComposing))})(e)&&(r||t)&&j&&(e.preventDefault(),_({fromUi:!0}),o&&w.submitForm(n,O))}),[S,w,j,_,O]),z={width:C},{height:B,placeholder:U,formId:N}=S,K=(0,p.Ml)({formId:N})?w.allowFormEnterToSubmit(N):j,V=I&&C>$.breakpoints.hideWidgetDetails;return(0,g.jsxs)("div",{className:"stTextArea","data-testid":"stTextArea",style:z,children:[(0,g.jsx)(u.L,{label:S.label,disabled:a,labelVisibility:(0,p.yv)(null===(r=S.labelVisibility)||void 0===r?void 0:r.value),htmlFor:F,children:S.help&&(0,g.jsx)(c.j,{children:(0,g.jsx)(d.A,{content:S.help,placement:f.W.TOP_RIGHT})})}),(0,g.jsx)(o.A,{value:null!==E&&void 0!==E?E:"",placeholder:U,onBlur:A,onFocus:D,onChange:R,onKeyDown:L,"aria-label":S.label,disabled:a,id:F,overrides:{Input:{style:{lineHeight:$.lineHeights.inputWidget,height:B?`${B}px`:"",minHeight:$.sizes.largestElementHeight,resize:"vertical","::placeholder":{opacity:"0.7"},paddingRight:$.spacing.lg,paddingLeft:$.spacing.lg,paddingBottom:$.spacing.lg,paddingTop:$.spacing.lg}},Root:{props:{"data-testid":"stTextAreaRootElement"},style:{borderLeftWidth:$.sizes.borderWidth,borderRightWidth:$.sizes.borderWidth,borderTopWidth:$.sizes.borderWidth,borderBottomWidth:$.sizes.borderWidth}}}}),V&&(0,g.jsx)(s.A,{dirty:j,value:null!==E&&void 0!==E?E:"",maxLength:S.maxChars,type:"multiline",inForm:(0,p.Ml)({formId:N}),allowEnterToSubmit:K})]})},w=(0,n.memo)(S)},3101:(e,t,r)=>{"use strict";r.d(t,{_:()=>a,t:()=>l});var n=r(58878),o=r(34752),i=r(25571);function a(e){let{getStateFromWidgetMgr:t,getDefaultState:r,updateWidgetMgrState:a,element:l,widgetMgr:s,fragmentId:u,onFormCleared:c}=e;const[d,f]=(0,n.useState)((()=>{var e;return null!==(e=t(s,l))&&void 0!==e?e:r(s,l)})),[p,m]=(0,n.useState)({value:d,fromUi:!1});(0,n.useEffect)((()=>{(0,i.hX)(p)||(m(null),f(p.value),a(l,s,p,u))}),[p,a,l,s,u]);const g=(0,n.useCallback)((()=>{m({value:r(s,l),fromUi:!0}),null===c||void 0===c||c()}),[m,l,r,s,c]);return(0,o.X)({widgetMgr:s,element:l,onFormCleared:g}),[d,m]}function l(e){let{getStateFromWidgetMgr:t,getDefaultStateFromProto:r,getCurrStateFromProto:o,updateWidgetMgrState:i,element:l,widgetMgr:s,fragmentId:u,onFormCleared:c}=e;const d=(0,n.useCallback)(((e,t)=>r(t)),[r]),[f,p]=a({getStateFromWidgetMgr:t,getDefaultState:d,updateWidgetMgrState:i,element:l,widgetMgr:s,fragmentId:u,onFormCleared:c});return(0,n.useEffect)((()=>{l.setValue&&(l.setValue=!1,p({value:o(l),fromUi:!1}))}),[l,o,p]),[f,p]}},94928:(e,t,r)=>{"use strict";r.d(t,{A:()=>x});var n=r(58878),o=r(35331),i=r(18648),a=r(92850),l=r(57224),s=r(81301);function u(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function c(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?u(Object(r),!0).forEach((function(t){d(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):u(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function d(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var f=(0,l.I4)("div",(function(e){return c(c({},(0,s.vt)(c(c({$positive:!1},e),{},{$hasIconTrailing:!1}))),{},{width:e.$resize?"fit-content":"100%"})}));f.displayName="StyledTextAreaRoot",f.displayName="StyledTextAreaRoot";var p=(0,l.I4)("div",(function(e){return(0,s.EO)(c({$positive:!1},e))}));p.displayName="StyledTextareaContainer",p.displayName="StyledTextareaContainer";var m=(0,l.I4)("textarea",(function(e){return c(c({},(0,s.n)(e)),{},{resize:e.$resize||"none"})}));function g(e){return g="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},g(e)}function h(){return h=Object.assign?Object.assign.bind():function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var n in r)Object.prototype.hasOwnProperty.call(r,n)&&(e[n]=r[n])}return e},h.apply(this,arguments)}function y(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!==typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,o,i=[],a=!0,l=!1;try{for(r=r.call(e);!(a=(n=r.next()).done)&&(i.push(n.value),!t||i.length!==t);a=!0);}catch(s){l=!0,o=s}finally{try{a||null==r.return||r.return()}finally{if(l)throw o}}return i}(e,t)||function(e,t){if(!e)return;if("string"===typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return b(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function v(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,n.key,n)}}function S(e,t){return S=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},S(e,t)}function w(e){var t=function(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=C(e);if(t){var o=C(this).constructor;r=Reflect.construct(n,arguments,o)}else r=n.apply(this,arguments);return function(e,t){if(t&&("object"===g(t)||"function"===typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return O(e)}(this,r)}}function O(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function C(e){return C=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},C(e)}function F(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}m.displayName="StyledTextarea",m.displayName="StyledTextarea";var j=function(e){!function(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&S(e,t)}(u,e);var t,r,l,s=w(u);function u(){var e;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,u);for(var t=arguments.length,r=new Array(t),n=0;n<t;n++)r[n]=arguments[n];return F(O(e=s.call.apply(s,[this].concat(r))),"state",{isFocused:e.props.autoFocus||!1}),F(O(e),"onFocus",(function(t){e.setState({isFocused:!0}),e.props.onFocus(t)})),F(O(e),"onBlur",(function(t){e.setState({isFocused:!1}),e.props.onBlur(t)})),e}return t=u,(r=[{key:"render",value:function(){var e=this.props.overrides,t=void 0===e?{}:e,r=y((0,o._O)(t.Root,f),2),l=r[0],s=r[1],u=(0,o.Qp)({Input:{component:m},InputContainer:{component:p}},t);return n.createElement(l,h({"data-baseweb":"textarea",$isFocused:this.state.isFocused,$isReadOnly:this.props.readOnly,$disabled:this.props.disabled,$error:this.props.error,$positive:this.props.positive,$required:this.props.required,$resize:this.props.resize},s),n.createElement(i.A,h({},this.props,{type:a.GT.textarea,overrides:u,onFocus:this.onFocus,onBlur:this.onBlur,resize:this.props.resize})))}}])&&v(t.prototype,r),l&&v(t,l),Object.defineProperty(t,"prototype",{writable:!1}),u}(n.Component);F(j,"defaultProps",{autoFocus:!1,disabled:!1,readOnly:!1,error:!1,name:"",onBlur:function(){},onChange:function(){},onKeyDown:function(){},onKeyPress:function(){},onKeyUp:function(){},onFocus:function(){},overrides:{},placeholder:"",required:!1,rows:3,size:a.SK.default});const x=j},32698:(e,t,r)=>{var n=r(30136),o=0;e.exports=function(e){var t=++o;return n(e)+t}}}]);