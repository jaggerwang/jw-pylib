def get_pages(page_index, total, limit, show=10):
    page = {}
    page_num = max(int((total - 0.1) // limit), 0)
    page['page_num'] = page_num
    if page_index > 0:
        page['pre_index'] = page_index - 1
    if page_index < page_num:
        page['next_index'] = page_index + 1
    from_index = max(page_index - show // 2, 0)
    to_index = min(
        page_index + (show - min(show // 2, (page_index - from_index + 1))),
        page_num)
    if to_index - from_index < show:
        from_index = max(to_index - show + 1, 0)
    page['range_indexes'] = list(range(from_index, to_index+1))
    page['page_index'] = page_index

    return page
