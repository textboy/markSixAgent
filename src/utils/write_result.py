def write_result(latest_draw_no, result):
    if len(latest_draw_no.split('/')) > 0:
        result_file_path = f"memory/predict_result_{latest_draw_no.split('/')[0]}.txt"
        with open(result_file_path, 'a', encoding='utf-8') as f:
            f.write(result)
            f.write("\n" + "-" * 20 + "\n\n")
    else:
        print(f"ERROR: latest_draw_no format is unexpected: {latest_draw_no}")