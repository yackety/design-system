# Changelog

Mọi thay đổi của Suite design system, mới nhất ở trên. Ghi thay đổi vào **Unreleased** khi làm, chia theo *Breaking*, *Added*, *Changed*, *Deprecated*, *Fixed*.

## [Unreleased]

## [0.1.0] — 2026-11-26

Bản mẫu đầu tiên.

### Added
- Hợp đồng token `tokens/contract.json`: 40 màu, 3 bóng (theo chế độ sáng/tối), 5 token theme (font, bo góc), danh sách token admin khách hàng được đổi, 35 cặp tương phản phải đạt.
- Token cố định `tokens/base.json`: thang chữ, khoảng cách, chuyển động, z-index, 2 mức mật độ, danh sách font hỗ trợ tiếng Việt.
- 3 theme: `default`, `evergreen` (mẫu), `civic` (mẫu).
- `tools/build.mjs`: build `dist/`, kiểm tra theme, lệnh `new-theme` suy ra màu từ màu thương hiệu.
- CSS component tiền tố `s-`: button, form (input, select, textarea, checkbox, radio, switch, form grid), card, KPI, description list, badge, avatar, alert, banner, tabs, segmented, table (tự xếp thành thẻ khi hẹp), dialog và bottom sheet, drawer, menu, toast, app shell (sidebar, topbar, bottom nav), empty, skeleton, progress.
- Trang demo `demo/index.html`.
