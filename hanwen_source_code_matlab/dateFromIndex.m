function strDate = dateFromIndex(iIndex) 
	%[years,months] = meshgrid([1963:1:2040],[1:1:12]);
	%[years,months] = meshgrid([1930:1:2040],[1:1:12]);
	[years,months] = meshgrid([1919:1:2040],[1:1:12]);

	[i,j] = ind2sub(size(years),iIndex);
	strDate = sprintf('1-%d-%d',months(i,j),years(i,j));
end