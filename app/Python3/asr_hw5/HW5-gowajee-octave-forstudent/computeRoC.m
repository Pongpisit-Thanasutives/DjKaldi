function [FP,TP] = computeRoC(yesscores,noscores)
    allscores = [yesscores noscores];
    totalyes = length(yesscores);
    totalno = length(noscores);
    minsc = min(allscores);
    maxsc = max(allscores);
    thres = minsc:(maxsc-minsc)/100:maxsc;
    FP = zeros(length(thres),1);
    TP = zeros(length(thres),1);
    for i = 1:length(thres)
        TP(i) = sum(yesscores < thres(i))/totalyes;
        FP(i) = sum(noscores < thres(i))/totalno;
    end
endfunction
