
class HintMsg():
    not_found_user = [401, '操作失敗，查詢不到當前用戶的數據！']
    upload_not_allowed = [402, '當前賬號沒有上傳文件權限！']
    file_empty = [403, '上傳圖片失敗，未選擇文件！']
    user_delete = [404, '操作失敗，當前用戶已刪除！']
    user_unactivation = [405, '操作失敗，當前用戶未激活！']
    not_found_Task = [406, '該Task不存在或已刪除！']
    not_found_TaskType = [606, '該TaskType不存在或已刪除！']
    not_found_TenicalDoc = [607, '該TenicalDoc不存在或已刪除！']
    discu_content_empty = [407, '發表回復失敗，回復內容不能為空！']
    not_found_discussion = [408, '操作失敗，嘗試訪問的回復數據不存在！']
    topic_is_over = [409, '操作失敗！該主題已結束！']
    search_type_error = [410, '搜索失敗，選擇的類型錯誤！']
    search_content_empty = [411, '搜索的內容不能為空！']
    not_found_parentcategory = [412, '添加失敗！父級分類不存在！']
    not_found_category = [413, '操作失敗，嘗試訪問的分類數據不存在！']
    include_subcategories = [414, '操作失敗，不能刪除有子分類的分類！']
    authority_choose_error = [415, '保存失敗，選擇錯誤，請重試！']
    setting_input_error = [416, '保存失敗，參數輸入錯誤，請重試！']
    group_name_error = [417, '創建失敗，分組名稱不能少於3個字符']
    msg_empty_error = [418, '發送消息失敗，消息內容不能為空！']
    not_in_group = [419, '退出失敗，當前分組中查不到你的數據！']
    database_error = [500, 'Database Error!']
    illegal_visit = [501, '非法訪問！']

def get_result(hint):
    result = {}
    result['state'] = hint[0]
    result['message'] = hint[1]
    return result
