function lvg = leverage(book_assets, book_equity, market_equity)
% Calculates the standard approximation of leverage for a firm
% Parameters:
% book_assets The book assets of the firm
% book_equity The book equity of the firm
% market_equity The market equity for the firm

lvg = (book_assets - book_equity + market_equity)/market_equity; 
