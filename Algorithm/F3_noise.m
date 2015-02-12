% author: Ray Weng
% date modified: 23 . 01 . 2015
function noise_F3
% does F3 analytics for the following file
filename = 'dailies.csv';
% expects a csv of with headers "crspid","cusip","qdate","yield","bid","ask","matdt","couprt","datdt","name"

% for R2012a, R2013a edition of matlab with no readtable() function
% filename = 'd_small.csv'; % FOR TESTING
fid = fopen(filename);
[mycell, err] = textscan(fid,'%f%s%f%f%f%f%f%f%f%s', 'Delimiter', ',','HeaderLines',1);
fclose(fid);
% number of columns in the csv, by getting size of cell array from text scan
k = size(mycell);  % we use k because we can't inline operations
nCols = k(2);
% number of rows, by opening first element and finding size
k = size(mycell{1});
nRows = k(1)

C = cell(nRows, nCols); % we will construct a reasonable cell array from the textscanned data

% this loop builds a cell array that is human readable, for the input text
for y = 1:nCols
	dd = mycell(y);
	if isa(dd{1}(1),'double') % check first element
		for x = 1:nRows
			C{x,y} = dd{1}(x);
		end
	else % when cell contains char, get value using {} not the cell with ()
		for x = 1:nRows
			C{x,y} = dd{1}{x};
		end
	end
end

% NOW we have a MATRIX corresponding to the data from the loaded csv
% resultData = map_by_dates(C);
% write to CSV
filename = 'data_noise.csv';
fid = fopen(filename,'w');
fprintf(fid, '%s, %s\n','quoteDate','noise');

% our quote dates are still in matlab datenum format
% so we must loop and convert
%for i = 1:size(resultData)
%	qdate = datestr(resultData(i,1), 'yyyymmdd');
%	n = resultData(i, 2);
%	fprintf(fid, '%8s, %4.4f\n', qdate, n);
%end
resultData = map_by_dates(C);
fprintf('rw422end of script\n') % easier to search log

fclose(fid);
% dlmwrite(filename,resultData,'-append')
end % end main program function


% takes in the matrix C created from importing the CSV into matlab
% this function should, for each quote date, find the corresponding noise
% by mapping the model() function to each set of data 
% for each quote date
% should return a 2xN matrix of quote dates and noise
function noiseMatrix=map_by_dates(C)
	index = 0;
	noiseMatrix = [];

	%TODO: run loop and aggregate data for each quote date into a
	% get date time
	dateCol = 3;
	qdate = datenum(num2str(C{1,dateCol},8), 'yyyymmdd'); % verify

	k = size(C);
	nRows = k(1);
	firstIndexOfCurrentDate = 1;

	% loop through all data
	for index = 1:nRows
		currRowDate = C{index,dateCol};
		currRowDate = num2str(currRowDate, 8);
		currRowDate = datenum(currRowDate, 'yyyymmdd');
		if currRowDate ~= qdate
			subset = C(firstIndexOfCurrentDate:index - 1, :);

			% run modeling function for this qdate
			modelOutput = model(subset);
			% append results
			noiseMatrix = [ noiseMatrix; modelOutput ];

			% update qdate/firstIndex to next qdate
			qdate = currRowDate;
			firstIndexOfCurrentDate = index;
		end % end if
	end % end loop

	% check for last segment of quotes because above loop has off by one error
	if index ~= firstIndexOfCurrentDate
		subset = C(firstIndexOfCurrentDate:nRows, :); % get remainder of cell array
		modelOutput = model(subset);
		noiseMatrix = [ noiseMatrix; modelOutput ];
	end

end % end map_by_dates()



% return a pair? [DateNumber, noise (double)]
% this function should be called once for each quote date in our data set
% where the argument C is just the cell array from
% the csv restricted to a single quote date
% parameter C looks like: 
% [crspid] [cusip] [qdate] [yield] [...]
function matrix =model(C)
	fprintf('model(C) ') % print to output that we are modeling one quote date
	dateCol = 3; %quote date
	bidAskCol = 5; % just use bid price for now isntead of meadian [5 6]
	maturityCol = 1; % we are obligated to use crspid column, which is YYYYMMDD.TCCCCE
	% which we parse when we convert to matrix
	couponCol = 8;
	datedDateCol = 9;
	yieldCol = 4;
	% data relevant to nelson siegel svensson model;
	rhsCols = [ maturityCol bidAskCol couponCol yieldCol ];
	k = size(C);
	nRows = k(1);

	rhs = C(:,rhsCols); % cell array of data relevant to svensson model
	% rhs looks like a cell array:
	% [settle] [maturity] [price] [coupon]
	% [settle] [maturity] [price] [coupon]

	% but we want it to look like a matrix of doubles

	% [settle maturity price coupon]
	% [settle maturity price coupon]

	% so now we clean up rhs to match that form
	% there are supposed to be four values
	qdate = C(1,dateCol); % settle date will just be quote date, which should be uniform
	% for all data in this set
	qdate = num2str(qdate{1}, 8);
	fprintf('for date %s\n', qdate); % print quote date of model to output
	qdate = datenum(qdate, 'yyyymmdd');

	% instruments will also contain yield column in addition to required fields
	% for the Svensson model
	% we include yield to make it easier in the next step to compare
	% model-predicted yields with actual yields.

	instruments = []; % clear it every time we run the function because we are appending

	instruments = [ qdate datenum(num2str(rhs{1,1},8),'yyyymmdd') rhs{1,2} rhs{1,3}*.01 rhs{1,4}];
	for y = 2:nRows % start with a seed for instruments table, then continue
		zz = [qdate datenum( num2str(rhs{y,1}, 8), 'yyyymmdd') rhs{y,2} rhs{y,3} rhs{y,4}];
		instruments = [instruments;zz];
	end

	% instruments = [ settle maturity cleanprice couponrate ] as expected by
	% IRFunctionCurve.fitSvensson() parameters
	% i think it is a matrix of doubles

	% zero coupon model, curve settle date, instruments (all bond data for that day)
	% using first four columns of the instruments matrix/array
	SvenssonModel = IRFunctionCurve.fitSvensson('Zero', qdate, instruments(:,1:4));
	% now we have to loop through every bond instrument,
	% find ones with maturity between 1 and 10 years per F3 paper
	% find squared difference between model par yield and actual reported yield

	% 2 x N matrix of maturity date and actual yield
	actualYields = instruments(:,[2 5]);
	noise = noiseRMSE(qdate, SvenssonModel, actualYields);
	matrix = [qdate noise]; % return date and noise value
end
% end model()



% qdate is a DATENUM of the quote date
% SvenssonModel is an IRFunctionCurve
% actualYields is a 2xN matrix of maturity date (DATENUM) and yields (double)
% given all the bond instruments transcated on the quote date,
% find the noise of all the instruments with maturities between 1 and 10 years
% by finding the model predicted yield versus the actual yield
% and calculating the RMSE
% return noise (RMSE) as a double
function noise = noiseRMSE(qdate, SvenssonModel, actualYields)
	ONE_YEAR = 364; % days
	TEN_YEAR = 3650; % days
	YIELD_THRESHOLD = 0.0100; % percent yield
	% predictedYields = getParYields(SvenssonModel, actualYields(:,1))


	% check maturities ; only model bonds within 1 and 10 year expiration
	nRows = size(actualYields);
	% rows to delete where maturity date is not within the bounds,
	% or yield is unlikely
	rowsToDelete = [];
	for i = 1:nRows
		if actualYields(i,1) < qdate + ONE_YEAR || actualYields(i,1) > qdate + TEN_YEAR
			rowsToDelete = [rowsToDelete i];
		elseif (abs(actualYields(i,2)) > YIELD_THRESHOLD)
			% check if actual yield from data is clean
			rowsToDelete = [rowsToDelete i];
		end
	end
	actualYields(rowsToDelete,:) = []; % actually delete the rows that do not meet requirements
	% actualYields only has maturity date and yields of desired maturity bonds

	% begin testing
	predictedYields = [];
	for i = 1:size(actualYields)
		predictedYields = [predictedYields; getParYields(SvenssonModel, actualYields(i,1))];
	end
	% end testing

	% y = [ maturity date  actualYields predictedYields]
	y = [ actualYields predictedYields ];

	noise = rms(y(:,3) - y(:,2)); % return noise value

	filename='data_noise.csv';
	fid = fopen(filename,'a');
	qdate = datestr(qdate, 'yyyymmdd');
	n = noise;
	fprintf(fid, '%8s, %4.4f\n', qdate, n)
	fclose(fid);
end
% end noiseRMSE()
% quit;
