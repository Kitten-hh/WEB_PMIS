/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./ScheduleApp/static/ScheduleApp/source/vue_page/Components/PoolLayout.js":
/*!*********************************************************************************!*\
  !*** ./ScheduleApp/static/ScheduleApp/source/vue_page/Components/PoolLayout.js ***!
  \*********************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (__WEBPACK_DEFAULT_EXPORT__)\n/* harmony export */ });\nclass PoolLayout extends go.GridLayout {\n  constructor() {\n    super();\n    this.MINLENGTH = 200; // this controls the minimum length of any swimlane\n    this.MINBREADTH = 100; // this controls the minimum breadth of any non-collapsed swimlane\n    this.cellSize = new go.Size(1, 1);\n    this.wrappingColumn = Infinity;\n    this.wrappingWidth = Infinity;\n    this.spacing = new go.Size(0, 0);\n    this.alignment = go.GridLayout.Position;\n  }\n  doLayout(coll) {\n    const diagram = this.diagram;\n    if (diagram === null) return;\n    diagram.startTransaction(\"PoolLayout\");\n    // make sure all of the Group Shapes are big enough\n    const minlen = this.computeMinPoolLength();\n    diagram.findTopLevelGroups().each(lane => {\n      if (!(lane instanceof go.Group)) return;\n      const shape = lane.selectionObject;\n      if (shape !== null) {\n        // change the desiredSize to be big enough in both directions\n        const sz = this.computeLaneSize(lane);\n        shape.width = !isNaN(shape.width) ? Math.max(shape.width, sz.width) : sz.width;\n        // if you want the height of all of the lanes to shrink as the maximum needed height decreases:\n        shape.height = minlen;\n        // if you want the height of all of the lanes to remain at the maximum height ever needed:\n        //shape.height = (isNaN(shape.height) ? minlen : Math.max(shape.height, minlen));\n        const cell = lane.resizeCellSize;\n        if (!isNaN(shape.width) && !isNaN(cell.width) && cell.width > 0) shape.width = Math.ceil(shape.width / cell.width) * cell.width;\n        if (!isNaN(shape.height) && !isNaN(cell.height) && cell.height > 0) shape.height = Math.ceil(shape.height / cell.height) * cell.height;\n      }\n    });\n    // now do all of the usual stuff, according to whatever properties have been set on this GridLayout\n    super.doLayout(coll);\n    diagram.commitTransaction(\"PoolLayout\");\n  }\n  // compute the minimum length of the whole diagram needed to hold all of the Lane Groups\n  computeMinPoolLength() {\n    let len = this.MINLENGTH;\n    myDiagram.findTopLevelGroups().each(lane => {\n      const holder = lane.placeholder;\n      if (holder !== null) {\n        const sz = holder.actualBounds;\n        len = Math.max(len, sz.height);\n      }\n    });\n    return len;\n  }\n\n  // compute the minimum size for a particular Lane Group\n  computeLaneSize(lane) {\n    // assert(lane instanceof go.Group);\n    const sz = new go.Size(lane.isSubGraphExpanded ? this.MINBREADTH : 1, this.MINLENGTH);\n    if (lane.isSubGraphExpanded) {\n      const holder = lane.placeholder;\n      if (holder !== null) {\n        const hsz = holder.actualBounds;\n        sz.width = Math.max(sz.width, hsz.width);\n      }\n    }\n    // minimum breadth needs to be big enough to hold the header\n    const hdr = lane.findObject(\"HEADER\");\n    if (hdr !== null) sz.width = Math.max(sz.width, hdr.actualBounds.width);\n    return sz;\n  }\n}\n// end PoolLayout class\n\n/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (PoolLayout);\n\n//# sourceURL=webpack://django_vue/./ScheduleApp/static/ScheduleApp/source/vue_page/Components/PoolLayout.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./ScheduleApp/static/ScheduleApp/source/vue_page/Components/PoolLayout.js"](0, __webpack_exports__, __webpack_require__);
/******/ 	
/******/ })()
;