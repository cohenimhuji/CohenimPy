
function [ ] = irfs2xls(filename, M_, oo_ )
    
    % save 
    % Nimrod Cohen 2021

    
temp_irfs = struct2cell(oo_.irfs)
irfs_values = vertcat(temp_irfs{:})'

xlswrite(filename, {'file name (.mod)' , M_.dname}	, 1, 'A1');
xlswrite(filename, {'file name (.mod)' , M_.fname}	, 1, 'A2');
xlswrite(filename, {'dynare_version' , M_.dynare_version}	, 1, 'A3');

xlswrite(filename, {'Parameters' ; 'Long Name'; 'Tex Name';'Value'}	, 'Parameters', 'A1');
xlswrite(filename, cellstr(M_.param_names')  	, 'Parameters', 'B1');
xlswrite(filename, cellstr(M_.param_names_long')  	, 'Parameters', 'B2');
xlswrite(filename, cellstr(M_.param_names_tex')  	, 'Parameters', 'B3');
xlswrite(filename, [M_.params'] 	, 'Parameters', 'B4'); 

xlswrite(filename, {'Endo Varibles' ; 'Long Name'; 'Tex Name';'oo_.vr_list';'oo_.steady_state';'oo_.mean'} , 'Endo', 'A1');
xlswrite(filename, cellstr(M_.endo_names') 	, 'Endo', 'B1');
xlswrite(filename, cellstr(M_.endo_names_long') 	, 'Endo', 'B2');
xlswrite(filename, cellstr(M_.endo_names_tex') 	, 'Endo', 'B3');
xlswrite(filename, oo_.var_list' 	, 'Endo', 'B4');
xlswrite(filename, oo_.steady_state', 'Endo', 'B5');
xlswrite(filename, oo_.mean', 'Endo', 'B6');

% M_.exo_names_long, 
    %  M_.exo_names_tex, 
    %  M_.exo_names
xlswrite(filename, {'Period'} , 'IRFs', 'A1');
xlswrite(filename, [0:20]' , 'IRFs','A2');
xlswrite(filename, fieldnames(oo_.irfs)' , 'IRFs','B1');
xlswrite(filename, irfs_values , 'IRFs','B2');

end