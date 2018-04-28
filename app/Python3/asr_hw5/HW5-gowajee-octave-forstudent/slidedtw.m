function [distances] = slidedtw(temp,test)
    testind = 1;
    lentest = size(test,2);
    lentemp = size(temp,2);
    globalcon = 50;
    computeind = 1;
    while testind + lentemp + globalcon < lentest
        %printf('test %d\n',testind);
        distances(computeind) = compute_dtw(temp,test(:,testind:testind+lentemp+globalcon));
        testind = testind+round(globalcon/2);
        computeind = computeind+1;
    end
end
