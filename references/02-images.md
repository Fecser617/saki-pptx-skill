# 02 专业图像的裁剪与等比例放置

## 裁剪（像素）
1. 源图从本轮用户上传原文件读取，不重复截图、不低质量保存。
2. 为各专业插图建立像素边界框 `(left,top,right,bottom)`，先检查像素坐标合法、宽/高 >0。
3. **故意保留一点安全边界**，尤其是节点、图表边缘、末端数据点、标注及图例，不能只看上半部。
4. 使用 `scripts/crop_contact_sheet.py` 可生成独立图块 + 原图裁剪范围标注图 + 缩略图检查页，人工确认每个图块没有丢内容。
5. 截图尽可能不包含旧边框和原文字；若裁剪无法去除附带文本，需避免在上层重复叠字。

## 强制适配
- 默认 **contain**：`scale=min(slotW/imageW,slotH/imageH)`，`placedW=imageW*scale`，`placedH=imageH*scale`，水平/垂直居中。
- 禁止 `width=slotW, height=slotH` 的直接强制拉伸，除非两者比例已经完全一致。
- 未授权不使用 `cover`，不使用高宽锁定但拉伸变形的方式填满区域。
- 裁剪图像是 PPT 的独立图片对象；不把整张页面栅格化。

### PptxGenJS 参照函数
```js
const { imageSizingContain } = require('pptxgenjs_helpers'); // 若当前环境提供帮助库
// 或先读取图片真实像素再用如下原理实现
function contain(pxW, pxH, boxX, boxY, boxW, boxH) {
  const s = Math.min(boxW/pxW, boxH/pxH);
  const w=pxW*s, h=pxH*s;
  return {x:boxX+(boxW-w)/2, y:boxY+(boxH-h)/2, w, h};
}
```
注：上例的 `imageSizingContain` 只是可能存在的帮助函数；以环境实际支持情况为准，不可假设其已加载。

## QA
- `validate_pptx.py` 自动检查插入后的可见图像宽高比误差是否不超过 1%。
- 机器检测不能判断图片是否从源图中裁掉了底部节点、头部文字或关键曲线；必须检查 contact sheet 和最终渲染。
- 原图本身清晰度低时，保持源图比例但说明限制，不做虚假高清处理。
