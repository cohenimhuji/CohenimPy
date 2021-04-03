
function [ ] = irfs2xls(filename, M_, oo_ )
    
    % save 
    % Nimrod Cohen 2021

    
temp_irfs = struct2cell(oo_.irfs)
irfs_values = vertcat(temp_irfs{:})'

xlswrite(filename, {'file name (.mod)' , M_.dname}	, 'model', 'A1');
xlswrite(filename, {'file name (.mod)' , M_.fname}	, 'model', 'A2');
xlswrite(filename, {'dynare_version' , M_.dynare_version}	, 'model', 'A3');

xlswrite(filename, {'Parameters ' , 'Long Name', 'tex name','Value'}	, 'model', 'A7');
xlswrite(filename, cellstr(M_.param_names)  	, 'model', 'A8');
xlswrite(filename, cellstr(M_.param_names_long)  	, 'model', 'B8');
xlswrite(filename, cellstr(M_.param_names_tex)  	, 'model', 'C8');
xlswrite(filename, [M_.params] 	, 'model', 'D8'); 
    % M_.exo_names_long, 
    %  M_.exo_names_tex, 
    %  M_.exo_names
xlswrite(filename, {'Varibles'} , 'output', 'A1');
xlswrite(filename, cellstr(M_.endo_names') 	, 'output', 'B1');
xlswrite(filename, cellstr(M_.endo_names_long') 	, 'output', 'B2');
xlswrite(filename, cellstr(M_.endo_names_tex') 	, 'output', 'B3');
xlswrite(filename, oo_.var_list' 	, 'output', 'B4');
xlswrite(filename, fieldnames(oo_.irfs)' , 'output','B5');

xlswrite(filename, {'Values'} , 'output', 'A6');
xlswrite(filename, irfs_values , 'output','B6');

end