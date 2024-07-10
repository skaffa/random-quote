import os
from pathlib import Path

def calculate_statistics():
    directory_paths = ['static/images', 'all_quote_images', 'temp']
    all_statistics = []
    
    for directory_path in directory_paths:
        directory = Path(directory_path)
        files = list(directory.glob('*.webp'))

        if files:
            total_size = sum(file.stat().st_size for file in files)
            if total_size < 1024 * 1024:
                total_size_str = f'{total_size / 1024:.2f} KB'
            else:
                total_size_str = f'{total_size / (1024 * 1024):.2f} MB'
            
            statistics = {
                'directory': directory_path,
                'total_files': len(files),
                'total_size': total_size_str
            }

            if len(files) > 0:
                average_size = total_size / len(files)
                if average_size < 1024 * 1024:
                    average_size_str = f'{average_size / 1024:.2f} KB'
                else:
                    average_size_str = f'{average_size / (1024 * 1024):.2f} MB'
                statistics['average_size'] = average_size_str
            else:
                statistics['average_size'] = 'No files found in the directory.'
            
            all_statistics.append(statistics)
        else:
            all_statistics.append({
                'directory': directory_path,
                'total_files': 0,
                'total_size': 'No .webp files found in the directory.'
            })
    
    return all_statistics

def generate_html_file():
    statistics = calculate_statistics()

    html_content = '''
    <html>
    <head>
        <title>Statistics for .webp files</title>
        <style>
            body {
                background-color: #121212;
                color: #e0e0e0;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }
            h2 {
                color: #1de9b6;
            }
            p {
                color: #ffffff;
            }
            .stats-container {
                background-color: #1f1f1f;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stat {
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
    '''

    for stats in statistics:
        html_content += f'''
        <div class="stats-container">
            <h2>`{stats["directory"]}`</h2>
            <p class="stat">Total files: {stats["total_files"]}</p>
            <p class="stat">Total size: {stats["total_size"]}</p>
            {f'<p class="stat">Average size: {stats["average_size"]}</p>' if 'average_size' in stats else ''}
        </div>
        '''

    html_content += '''
    </body>
    </html>
    '''

    return html_content

