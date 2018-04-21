function [yesd,nod] = computeall(temp,yeses,noes)
    % Since we dont know where "Gowajee" exactly is in each utterance,
    % we assume the smallest distance is the Gowajee location.
    yesd = zeros(1,length(yeses));
    for i = 1:length(yeses)
        printf('computing yes utterances #%d\n',i);
        yesd(i) = min(slidedtw(temp,yeses{1,i}));
    end
    % Every part of the noes has no Gowajee. We keep all the scores.
    nod = []
    for i = 1:length(noes)
        printf('computing no utterances #%d\n',i);
        nod = [nod slidedtw(temp,noes{1,i})];
    end
end
