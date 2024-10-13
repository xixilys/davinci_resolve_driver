import os
import shutil
import re
import subprocess
import configparser
from davinci_control import davinci_drive
def process_videos(folder_4k):
    # 正则表达式匹配文件夹名格式
    folder_pattern = r'(\d{6}_\w+)'

    # # 确定目标分辨率
    # target_resolution = '1080:1920'

    # # 创建output文件夹
    folder_output = os.path.join(folder_4k, 'output')
    os.makedirs(folder_output, exist_ok=True)

    # 遍历4K文件夹
    for folder_name in os.listdir(folder_4k):
        folder_path = os.path.join(folder_4k, folder_name)
        if os.path.isdir(folder_path) and re.match(folder_pattern, folder_name):
            print(f"正在处理文件夹：{folder_name}")
            # davinci_drive(folder_path,folder_output)
            
            # # 获取文件夹中的所有视频文件并排序，排除名字后缀带有-1080p的文件
            # video_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.mov') and not f.lower().endswith('-1080p.mp4')])
            
            # for index, filename in enumerate(video_files, start=1):
            #     print(filename)
            #     # 构建新的文件名
            #     new_filename = f"{folder_name}{index:02d}.mp4"
            #     src_path = os.path.join(folder_path, filename)
            #     dst_path = os.path.join(folder_path, new_filename)
                
            #     # 生成1080p视频
            #     new_1080p_filename = f"{folder_name}{index:02d}-1080p.mp4"
            #     dst_1080p = os.path.join(folder_path, new_1080p_filename)
                
            #     # 检查1080p视频是否已存在
            #     if not os.path.exists(dst_1080p):
            #         try:
            #             ffmpeg_command = f"ffmpeg -hwaccel cuda -i {src_path} -vf crop=3510:6240:(in_w-3510)/2:0,scale=1080:1920,lut3d=file=FLOG2_TO_709_PHANTOM.cube -c:v h264_nvenc -b:v 12M -pix_fmt yuv420p -c:a copy -color_range 1 -color_primaries 1 -color_trc 1 {dst_1080p}"
            #             print(f"正在生成居中裁剪的1080p视频并加载LUT：{new_1080p_filename}")
            #             subprocess.run(ffmpeg_command, shell=True, check=True)
            #         except subprocess.CalledProcessError:
            #             print(f"生成1080p视频时发生错误：{new_1080p_filename}")
            #             if os.path.exists(dst_1080p):
            #                 os.remove(dst_1080p)
            #                 print(f"已删除错误的1080p视频：{new_1080p_filename}")
            #     else:
            #         print(f"1080p视频已存在，跳过生成：{new_1080p_filename}")

            #     # 复制1080p视频到1080p文件夹（如果存在）
            #     if os.path.exists(dst_1080p):
            #         dst_1080p_copy = os.path.join(folder_1080p, new_1080p_filename)
            #         shutil.copy2(dst_1080p, dst_1080p_copy)
            #         print(f"已复制1080p视频到1080p文件夹：{new_1080p_filename}")
            #     else:
            #         print(f"1080p视频不存在或生成失败，跳过复制：{new_1080p_filename}")
            print("folder output is ")
            folder_output_last = os.path.join(folder_output, folder_name)
            print(folder_output_last)
            video_files = sorted([f for f in os.listdir(folder_output_last) if f.lower().endswith('.mp4') and not f.lower().endswith('-1080p.mp4')])
            for index, video_file in enumerate(video_files, start=1):
                new_name = f"{folder_name}_p{index}.mp4"  # 创建新的文件名
                old_file_path = os.path.join(folder_output_last, video_file)  # 原文件路径
                new_file_path = os.path.join(folder_output_last, new_name)  # 新文件路径 
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{video_file}' to '{new_name}'")
            

            print(f"文件夹 {folder_name} 处理完成")

def process_folders(folder_4k):
    # 读取xox.txt文件
    with open('xox.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 创建一个字典来存储团体和人名的映射
    group_name_map = {}
    for line in lines:
        content = line.strip()
        if content:
            parts = content.split('-')
            name = parts[-1]
            group = '-'.join(parts[:-1])
            group_name_map[name] = group
    
    # 遍历4K文件夹
    for folder_name in os.listdir(folder_4k):
        folder_path = os.path.join(folder_4k, folder_name)
        if os.path.isdir(folder_path):
            name = folder_name.split('-')[-1]
            if name in group_name_map:
                group = group_name_map[name]
                
                # 创建团体文件夹
                group_folder = os.path.join(folder_4k, group)
                os.makedirs(group_folder, exist_ok=True)
                
                # 创建人名文件夹
                name_folder = os.path.join(group_folder, name)
                os.makedirs(name_folder, exist_ok=True)
                
                # 移动文件夹到人名文件夹下
                new_path = os.path.join(name_folder, folder_name)
                shutil.move(folder_path, new_path)
                print(f"已移动文件夹 {folder_name} 到 {new_path}")


def read_config(config_file):
    # 创建一个配置解析器
    config = configparser.ConfigParser()
    
    # 读取配置文件
    config.read(config_file)
    
    # 提取参数
    project_name = config.get('Settings', 'projectName')
    framerate = config.get('Settings', 'framerate')
    width = config.get('Settings', 'width')
    height = config.get('Settings', 'height')
    grade_mode = config.getint('Settings', 'gradeMode')
    render_preset_name = config.get('Settings', 'renderPresetName')
    media_path = config.get('Settings', 'mediaPath')
    output_path = config.get('Settings', 'outputPath')
    drx_path = config.get('Settings', 'drxPath')
    
    # 返回参数作为字典
    return {
        'projectName': project_name,
        'framerate': framerate,
        'width': width,
        'height': height,
        'gradeMode': grade_mode,
        'renderPresetName': render_preset_name,
        'mediaPath': media_path,
        'outputPath': output_path,
        'drxPath': drx_path
    }



if __name__ == "__main__":
    print("程序开始运行")
    mediaPath = "/mnt/data/ddddddd/special_tools/vedio_development/240922"  # 媒体文件夹路径

    print(f"4K文件夹：{mediaPath}")
    process_videos(mediaPath)
    # process_folders(folder_4k)
    print("程序执行完毕")